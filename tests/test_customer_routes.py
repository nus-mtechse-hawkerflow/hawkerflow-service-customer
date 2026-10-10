import json
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest
from fastapi import Request

from endpoints.customer_routes import (
    check_account_exist,
    cust_router,
    get_user_details,
    get_user_service,
    register_user,
    update_order,
)
from models.customer_account import CustomerAccount
from models.customer_details import CustomerDetails
from models.customer_order_details import CustomerOrderDetails
from user_service.user_service import UserService


class TestCustomerRoutes:
    def test_get_user_service_dependency(self):
        mock_request = MagicMock(spec=Request)
        mock_service = MagicMock(spec=UserService)
        mock_request.app.state.user_service = mock_service

        service = get_user_service(mock_request)
        assert service is mock_service

    @pytest.mark.anyio
    async def test_register_user_endpoint(self, sample_customer_details: CustomerDetails):
        mock_user_service = MagicMock(spec=UserService)
        mock_customer = MagicMock()
        mock_customer.f_id = 1
        mock_customer.f_first_name = sample_customer_details.first_name
        mock_customer.f_last_name = sample_customer_details.last_name
        mock_customer.f_created_at = datetime.now(timezone.utc)
        mock_user_service.register_customer.return_value = mock_customer

        response = await register_user(sample_customer_details, mock_user_service)

        mock_user_service.register_customer.assert_called_once_with(sample_customer_details)
        assert response.status_code == 200

        data = json.loads(response.body)
        assert data["cust_id"] == 1
        assert (
            data["cust_name"]
            == f"{sample_customer_details.first_name} {sample_customer_details.last_name}"
        )
        assert "created_at" in data

    @pytest.mark.anyio
    async def test_check_account_exist_endpoint(
        self, sample_customer_account: CustomerAccount
    ):
        mock_user_service = MagicMock(spec=UserService)
        mock_user_service.check_account_exist.return_value = True

        response = await check_account_exist(sample_customer_account, mock_user_service)

        mock_user_service.check_account_exist.assert_called_once_with(sample_customer_account)
        assert response.status_code == 200

        data = json.loads(response.body)
        assert data["account_exist"] is True

    @pytest.mark.anyio
    async def test_get_user_details_endpoint(self):
        mock_user_service = MagicMock(spec=UserService)
        expected_details = {
            "cust_id": "sub-100",
            "cust_name": "Alice Wong",
            "last_login": "2026-10-10 12:00:00",
        }
        mock_user_service.get_customer_details.return_value = expected_details

        response = await get_user_details("sub-100", mock_user_service)

        mock_user_service.get_customer_details.assert_called_once_with("sub-100")
        assert response.status_code == 200

        data = json.loads(response.body)
        assert data == expected_details

    @pytest.mark.anyio
    async def test_update_order_endpoint(self, sample_order_details: CustomerOrderDetails):
        mock_user_service = MagicMock(spec=UserService)

        response = await update_order(sample_order_details, mock_user_service)

        mock_user_service.update_cust_order.assert_called_once_with(sample_order_details)
        assert response.status_code == 200

        data = json.loads(response.body)
        assert data == {"message": "Customer Order Updated"}

    def test_router_configuration(self):
        routes = {route.path: route.methods for route in cust_router.routes}
        assert "/v1/customer/register" in routes
        assert "POST" in routes["/v1/customer/register"]
        assert "/v1/customer/check_account_exist" in routes
        assert "POST" in routes["/v1/customer/check_account_exist"]
        assert "/v1/customer/user/{cust_sub}" in routes
        assert "GET" in routes["/v1/customer/user/{cust_sub}"]
        assert "/v1/customer/user/update_order" in routes
        assert "POST" in routes["/v1/customer/user/update_order"]

from unittest.mock import MagicMock

from models.customer_account import CustomerAccount
from models.customer_details import CustomerDetails
from models.customer_order_details import CustomerOrderDetails
from repository.customer_orders_repo import CustomerOrdersRepo
from repository.customer_repo import CustomerRepo
from user_service.user_service import UserService


class TestUserService:
    def test_register_customer_delegation(self, sample_customer_details: CustomerDetails):
        mock_user_repo = MagicMock(spec=CustomerRepo)
        mock_order_repo = MagicMock(spec=CustomerOrdersRepo)
        mock_customer = MagicMock()
        mock_user_repo.create_customer.return_value = mock_customer

        service = UserService(mock_user_repo, mock_order_repo)
        result = service.register_customer(sample_customer_details)

        mock_user_repo.create_customer.assert_called_once_with(sample_customer_details)
        assert result is mock_customer

    def test_check_account_exist_delegation(self, sample_customer_account: CustomerAccount):
        mock_user_repo = MagicMock(spec=CustomerRepo)
        mock_order_repo = MagicMock(spec=CustomerOrdersRepo)
        mock_user_repo.check_account_exist.return_value = True

        service = UserService(mock_user_repo, mock_order_repo)
        result = service.check_account_exist(sample_customer_account)

        mock_user_repo.check_account_exist.assert_called_once_with(sample_customer_account)
        assert result is True

    def test_get_customer_details_delegation(self):
        mock_user_repo = MagicMock(spec=CustomerRepo)
        mock_order_repo = MagicMock(spec=CustomerOrdersRepo)
        expected_details = {"cust_id": "sub-123", "cust_name": "Test User"}
        mock_user_repo.get_customer_details.return_value = expected_details

        service = UserService(mock_user_repo, mock_order_repo)
        result = service.get_customer_details("sub-123")

        mock_user_repo.get_customer_details.assert_called_once_with("sub-123")
        assert result == expected_details

    def test_update_cust_order_delegation(self, sample_order_details: CustomerOrderDetails):
        mock_user_repo = MagicMock(spec=CustomerRepo)
        mock_order_repo = MagicMock(spec=CustomerOrdersRepo)
        mock_response = [{"order_id": 5001, "order_status": "PENDING"}]
        mock_order_repo.update_cust_order.return_value = mock_response

        service = UserService(mock_user_repo, mock_order_repo)
        result = service.update_cust_order(sample_order_details)

        mock_order_repo.update_cust_order.assert_called_once_with(sample_order_details)
        assert result == mock_response

    def test_service_integration_with_real_repositories(
        self,
        user_service: UserService,
        sample_customer_details: CustomerDetails,
        sample_customer_account: CustomerAccount,
        sample_order_details: CustomerOrderDetails,
    ):
        # 1. Register customer
        customer = user_service.register_customer(sample_customer_details)
        assert customer.f_cust_sub == sample_customer_details.customer_sub

        # 2. Check account exist
        assert user_service.check_account_exist(sample_customer_account) is True

        # 3. Update order
        order_res = user_service.update_cust_order(sample_order_details)
        assert len(order_res) == 2

        # 4. Get customer details
        details = user_service.get_customer_details(sample_customer_details.customer_sub)
        assert details["cust_id"] == sample_customer_details.customer_sub
        assert len(details["past_orders"]["orders"]) == 2

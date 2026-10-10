import pytest
from pydantic import ValidationError

from models.customer_account import CustomerAccount
from models.customer_details import CustomerDetails
from models.customer_order_details import CustomerOrderDetails, Dish, Order


class TestCustomerDetails:
    def test_valid_customer_details(self):
        details = CustomerDetails(
            first_name="Alice",
            last_name="Wong",
            email="alice.wong@example.com",
            phone_number="+6598765432",
            customer_sub="sub-alice-01",
        )
        assert details.first_name == "Alice"
        assert details.last_name == "Wong"
        assert details.email == "alice.wong@example.com"
        assert details.phone_number == "+6598765432"
        assert details.customer_sub == "sub-alice-01"

    def test_invalid_email_raises_validation_error(self):
        with pytest.raises(ValidationError):
            CustomerDetails(
                first_name="Alice",
                last_name="Wong",
                email="not-an-email",
                phone_number="+6598765432",
                customer_sub="sub-alice-01",
            )

    def test_missing_required_fields_raises_validation_error(self):
        with pytest.raises(ValidationError):
            CustomerDetails(
                first_name="Alice",
                last_name="Wong",
            )


class TestCustomerAccount:
    def test_valid_customer_account(self):
        account = CustomerAccount(
            phone_number="+6598765432",
            email="alice.wong@example.com",
        )
        assert account.phone_number == "+6598765432"
        assert account.email == "alice.wong@example.com"

    def test_invalid_email_raises_validation_error(self):
        with pytest.raises(ValidationError):
            CustomerAccount(
                phone_number="+6598765432",
                email="invalid-email",
            )

    def test_missing_fields_raises_validation_error(self):
        with pytest.raises(ValidationError):
            CustomerAccount(phone_number="+6598765432")


class TestCustomerOrderDetails:
    def test_valid_dish_and_order(self):
        dish = Dish(dish_id=1, dish_name="Laksa", quantity=1, price=5.50)
        assert dish.dish_id == 1
        assert dish.dish_name == "Laksa"
        assert dish.quantity == 1
        assert dish.price == 5.50

        order = Order(stall_id=10, dishes=[dish])
        assert order.stall_id == 10
        assert len(order.dishes) == 1

    def test_valid_customer_order_details(self):
        dish = Dish(dish_id=1, dish_name="Laksa", quantity=2, price=11.0)
        order = Order(stall_id=10, dishes=[dish])
        cust_order = CustomerOrderDetails(
            order_id=999,
            cust_sub="sub-123",
            orders=[order],
            total_price=11.0,
            status="COMPLETED",
        )
        assert cust_order.order_id == 999
        assert cust_order.cust_sub == "sub-123"
        assert cust_order.total_price == 11.0
        assert cust_order.status == "COMPLETED"
        assert len(cust_order.orders) == 1
        assert cust_order.orders[0].dishes[0].dish_name == "Laksa"

    def test_invalid_customer_order_details_missing_fields(self):
        with pytest.raises(ValidationError):
            CustomerOrderDetails(order_id=999)

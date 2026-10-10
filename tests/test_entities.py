from datetime import datetime, timezone

from entities.customer import Customer
from entities.customer_loyalty import CustomerLoyalty
from entities.customer_orders import CustomerOrders


class TestCustomerEntity:
    def test_customer_creation_defaults(self):
        before = datetime.now(timezone.utc)
        customer = Customer(
            f_cust_sub="cust-100",
            f_first_name="Bob",
            f_last_name="Lee",
            f_email="bob.lee@example.com",
            f_phone_number="+6590001111",
        )
        after = datetime.now(timezone.utc)

        assert customer.f_id is None
        assert customer.f_cust_sub == "cust-100"
        assert customer.f_first_name == "Bob"
        assert customer.f_last_name == "Lee"
        assert customer.f_email == "bob.lee@example.com"
        assert customer.f_phone_number == "+6590001111"
        assert before <= customer.f_created_at <= after
        assert before <= customer.f_last_login <= after
        assert customer.customer_loyalty == []
        assert customer.customer_orders == []

    def test_customer_tablename(self):
        assert Customer.__tablename__ == "customer"


class TestCustomerLoyaltyEntity:
    def test_customer_loyalty_defaults(self):
        loyalty = CustomerLoyalty(
            f_cust_sub="cust-100",
            f_loyalty_points=50,
        )
        assert loyalty.f_cust_sub == "cust-100"
        assert loyalty.f_loyalty_tier == "BRONZE"
        assert loyalty.f_loyalty_points == 50
        assert loyalty.f_last_order_at is None

    def test_customer_loyalty_tablename(self):
        assert CustomerLoyalty.__tablename__ == "customer_loyalty"


class TestCustomerOrdersEntity:
    def test_customer_orders_creation(self):
        before = datetime.now(timezone.utc)
        order = CustomerOrders(
            f_order_id=1,
            f_cust_sub="cust-100",
            f_dish_id=10,
            f_dish_name="Hainanese Chicken Rice",
            f_quantity=1,
            f_order_price=5.0,
            f_order_status="CONFIRMED",
        )
        after = datetime.now(timezone.utc)

        assert order.f_id is None
        assert order.f_order_id == 1
        assert order.f_cust_sub == "cust-100"
        assert order.f_dish_id == 10
        assert order.f_dish_name == "Hainanese Chicken Rice"
        assert order.f_quantity == 1
        assert order.f_order_price == 5.0
        assert order.f_order_status == "CONFIRMED"
        assert before <= order.f_order_date <= after

    def test_customer_orders_tablename(self):
        assert CustomerOrders.__tablename__ == "customer_orders"

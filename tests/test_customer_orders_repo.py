from sqlmodel import Session, select

from entities.customer_orders import CustomerOrders
from models.customer_order_details import CustomerOrderDetails
from repository.customer_orders_repo import CustomerOrdersRepo


class TestCustomerOrdersRepo:
    def test_update_cust_order_creates_new_orders_when_none_exist(
        self,
        customer_orders_repo: CustomerOrdersRepo,
        sample_order_details: CustomerOrderDetails,
        in_memory_engine,
    ):
        result = customer_orders_repo.update_cust_order(sample_order_details)

        assert len(result) == 2
        assert result[0]["order_id"] == 5001
        assert result[0]["order_status"] == "PENDING"
        assert result[0]["dish_name"] == "Chicken Rice"
        assert result[0]["quantity"] == 2
        assert result[0]["order_price"] == 10.0
        assert result[0]["order_date"] is not None

        assert result[1]["order_id"] == 5001
        assert result[1]["order_status"] == "PENDING"
        assert result[1]["dish_name"] == "Iced Lemon Tea"

        # Verify persisted in database
        with Session(in_memory_engine) as session:
            orders_in_db = session.exec(
                select(CustomerOrders).where(CustomerOrders.f_order_id == 5001)
            ).all()
            assert len(orders_in_db) == 2

    def test_update_cust_order_updates_status_when_orders_exist(
        self,
        customer_orders_repo: CustomerOrdersRepo,
        sample_order_details: CustomerOrderDetails,
        in_memory_engine,
    ):
        # 1. First call inserts new records
        customer_orders_repo.update_cust_order(sample_order_details)

        # 2. Update status to "COMPLETED"
        updated_details = CustomerOrderDetails(
            order_id=sample_order_details.order_id,
            cust_sub=sample_order_details.cust_sub,
            orders=sample_order_details.orders,
            total_price=sample_order_details.total_price,
            status="COMPLETED",
        )
        result = customer_orders_repo.update_cust_order(updated_details)

        assert len(result) == 2
        assert result[0]["order_status"] == "COMPLETED"
        assert result[1]["order_status"] == "COMPLETED"

        # Verify DB records updated
        with Session(in_memory_engine) as session:
            orders_in_db = session.exec(
                select(CustomerOrders).where(CustomerOrders.f_order_id == 5001)
            ).all()
            for o in orders_in_db:
                assert o.f_order_status == "COMPLETED"

    def test_populate_cust_order(
        self,
        customer_orders_repo: CustomerOrdersRepo,
        sample_order_details: CustomerOrderDetails,
    ):
        entities = customer_orders_repo._populate_cust_order(sample_order_details)

        assert len(entities) == 2
        assert isinstance(entities[0], CustomerOrders)
        assert entities[0].f_order_id == 5001
        assert entities[0].f_cust_sub == "sub-cust-001"
        assert entities[0].f_dish_id == 101
        assert entities[0].f_dish_name == "Chicken Rice"
        assert entities[0].f_quantity == 2
        assert entities[0].f_order_price == 10.0
        assert entities[0].f_order_status == "PENDING"

        assert entities[1].f_dish_id == 102
        assert entities[1].f_dish_name == "Iced Lemon Tea"

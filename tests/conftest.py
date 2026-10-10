import pytest
from sqlmodel import SQLModel, create_engine

# Import entities to ensure SQLModel and SQLAlchemy metadata are registered
from models.customer_account import CustomerAccount
from models.customer_details import CustomerDetails
from models.customer_order_details import CustomerOrderDetails, Dish, Order
from repository.customer_orders_repo import CustomerOrdersRepo
from repository.customer_repo import CustomerRepo
from user_service.user_service import UserService


@pytest.fixture
def in_memory_engine():
    """Provides a fresh SQLite in-memory engine with all tables created."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def sample_customer_details() -> CustomerDetails:
    return CustomerDetails(
        first_name="Jane",
        last_name="Tan",
        email="jane.tan@example.com",
        phone_number="+6591234567",
        customer_sub="sub-cust-001",
    )


@pytest.fixture
def sample_customer_account() -> CustomerAccount:
    return CustomerAccount(
        phone_number="+6591234567",
        email="jane.tan@example.com",
    )


@pytest.fixture
def sample_order_details() -> CustomerOrderDetails:
    dish1 = Dish(dish_id=101, dish_name="Chicken Rice", quantity=2, price=10.0)
    dish2 = Dish(dish_id=102, dish_name="Iced Lemon Tea", quantity=1, price=2.5)
    order1 = Order(stall_id=1, dishes=[dish1, dish2])
    return CustomerOrderDetails(
        order_id=5001,
        cust_sub="sub-cust-001",
        orders=[order1],
        total_price=12.5,
        status="PENDING",
    )


@pytest.fixture
def customer_repo(in_memory_engine) -> CustomerRepo:
    return CustomerRepo(in_memory_engine)


@pytest.fixture
def customer_orders_repo(in_memory_engine) -> CustomerOrdersRepo:
    return CustomerOrdersRepo(in_memory_engine)


@pytest.fixture
def user_service(customer_repo, customer_orders_repo) -> UserService:
    return UserService(customer_repo, customer_orders_repo)

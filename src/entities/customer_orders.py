from datetime import datetime, timezone

from sqlmodel import SQLModel, Field, Relationship


class CustomerOrders(SQLModel, table=True):

    __tablename__ = "customer_orders"

    f_id: int = Field(default=None, primary_key=True)
    f_order_id: int = Field(index=True)
    f_cust_sub: str = Field(foreign_key="customer.f_cust_sub", index=True)
    f_dish_id: int
    f_dish_name: str
    f_quantity: int
    f_order_price: float
    f_order_status: str
    f_order_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    customer: "Customer" = Relationship(back_populates="customer_orders")

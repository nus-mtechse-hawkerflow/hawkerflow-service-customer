from datetime import datetime, timezone

from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship


class Customer(SQLModel, table=True):
    __tablename__ = "customer"

    f_id: int = Field(default=None, primary_key=True)
    f_cust_sub: str = Field(index=True, unique=True)
    f_first_name: str
    f_last_name: str
    f_email: EmailStr = Field(unique=True, index=True)
    f_phone_number: str = Field(unique=True, index=True)
    f_last_login: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    f_created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    customer_loyalty: list["CustomerLoyalty"] = Relationship(back_populates="customer")
    customer_orders: list["CustomerOrders"] = Relationship(back_populates="customer")

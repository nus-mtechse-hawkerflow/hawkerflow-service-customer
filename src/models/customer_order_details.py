from pydantic import BaseModel


class Dish(BaseModel):
    dish_id: int
    dish_name: str
    quantity: int
    price: float


class Order(BaseModel):
    stall_id: int
    dishes: list[Dish]


class CustomerOrderDetails(BaseModel):
    order_id: int
    cust_sub: str
    orders: list[Order]
    total_price: float
    status: str

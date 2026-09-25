from datetime import datetime, timezone

from sqlmodel import Session, select
from sqlalchemy import Engine

from entities.customer_loyalty import CustomerLoyalty
from entities.customer import Customer
from models.customer_account import CustomerAccount
from models.customer_details import CustomerDetails


class CustomerRepo:
    def __init__(self, engine: Engine):
        self._engine = engine

    def get_customer_by_email(self, email: str):
        with Session(self._engine) as session:
            statement = select(Customer).where(Customer.f_email == email)
            return session.exec(statement).first()

    def create_customer(self, customer_details: CustomerDetails):
        customer = Customer(
            f_email=customer_details.email,
            f_first_name=customer_details.first_name,
            f_last_name=customer_details.last_name,
            f_phone_number=customer_details.phone_number,
            f_cust_sub=customer_details.customer_sub
        )

        customer_loyalty = CustomerLoyalty(
            f_loyalty_tier="BRONZE",
            f_loyalty_points=0
        )

        customer.customer_loyalty.append(customer_loyalty)

        with Session(self._engine) as session:
            session.add(customer)
            session.commit()
            session.refresh(customer)

            return customer

    def update_customer(self, customer_details: CustomerDetails):
        with Session(self._engine) as session:
            customer = session.get(Customer, customer_details.email)
            customer.f_first_name = customer_details.first_name
            customer.f_last_name = customer_details.last_name
            customer.f_phone_number = customer_details.phone_number
            session.add(customer)
            session.commit()
            session.refresh(customer)
            return customer

    def check_account_exist(self, customer_account: CustomerAccount) -> bool:
        with Session(self._engine) as session:
            statement = select(Customer).where(
                (Customer.f_email == customer_account.email) &
                (Customer.f_phone_number == customer_account.phone_number)
            )
            result = session.exec(statement).first()
            return result is not None

    def get_customer_details(self, customer_sub: str):
        with Session(self._engine) as session:
            statement = select(Customer).where(Customer.f_cust_sub == customer_sub)
            customer = session.exec(statement).first()

            if customer is not None:
                customer_details = {
                    "cust_id": customer.f_cust_sub,
                    "cust_name": customer.f_first_name + " " + customer.f_last_name,
                    "last_login": customer.f_last_login.strftime("%Y-%m-%d %H:%M:%S"),
                    "past_orders": {
                        "orders": [
                            {
                                "order_id": order.f_order_id,
                                "order_name": order.f_order_name,
                                "order_quantity": order.f_order_quantity,
                                "order_price": order.f_order_price,
                                "order_status": order.f_order_status
                            } for order in customer.customer_orders
                        ]
                    }
                }
                customer.f_last_login = datetime.now(timezone.utc)
                session.add(customer)
                session.commit()
                session.refresh(customer)

                return customer_details

            return {
                "cust_id": customer_sub,
                "cust_name": None,
                "last_login": None
            }

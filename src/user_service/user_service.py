from models.customer_account import CustomerAccount
from models.customer_details import CustomerDetails
from models.customer_order_details import CustomerOrderDetails
from repository.customer_orders_repo import CustomerOrdersRepo
from repository.customer_repo import CustomerRepo
from entities.customer import Customer


class UserService:
    def __init__(self, user_repo: CustomerRepo, user_order_repo: CustomerOrdersRepo):
        self._repository = user_repo
        self._order_repository = user_order_repo

    def register_customer(self, customer_details: CustomerDetails) -> Customer:
        return self._repository.create_customer(customer_details)

    def check_account_exist(self, customer_account: CustomerAccount) -> bool:
        return self._repository.check_account_exist(customer_account)

    def get_customer_details(self, customer_sub: str) -> dict[str, str]:
        return self._repository.get_customer_details(customer_sub)

    def update_cust_order(self, order_details: CustomerOrderDetails) -> Customer:
        return self._order_repository.update_cust_order(order_details)


from sqlmodel import Session

from entities.customer_orders import CustomerOrders
from models.customer_account import CustomerAccount
from models.customer_details import CustomerDetails
from repository.customer_repo import CustomerRepo


class TestCustomerRepo:
    def test_create_customer(
        self,
        customer_repo: CustomerRepo,
        sample_customer_details: CustomerDetails,
        in_memory_engine,
    ):
        customer = customer_repo.create_customer(sample_customer_details)

        assert customer.f_id is not None
        assert customer.f_email == sample_customer_details.email
        assert customer.f_first_name == sample_customer_details.first_name
        assert customer.f_last_name == sample_customer_details.last_name
        assert customer.f_phone_number == sample_customer_details.phone_number
        assert customer.f_cust_sub == sample_customer_details.customer_sub

        # Verify CustomerLoyalty record was created and linked to this customer
        with Session(in_memory_engine) as session:
            from sqlmodel import select

            from entities.customer_loyalty import CustomerLoyalty

            loyalty = session.exec(
                select(CustomerLoyalty).where(
                    CustomerLoyalty.f_cust_sub == sample_customer_details.customer_sub
                )
            ).first()
            assert loyalty is not None
            assert loyalty.f_loyalty_tier == "BRONZE"
            assert loyalty.f_loyalty_points == 0

    def test_get_customer_by_email_found(
        self, customer_repo: CustomerRepo, sample_customer_details: CustomerDetails
    ):
        created = customer_repo.create_customer(sample_customer_details)
        found = customer_repo.get_customer_by_email(sample_customer_details.email)

        assert found is not None
        assert found.f_id == created.f_id
        assert found.f_cust_sub == sample_customer_details.customer_sub

    def test_get_customer_by_email_not_found(self, customer_repo: CustomerRepo):
        found = customer_repo.get_customer_by_email("unknown@example.com")
        assert found is None

    def test_check_account_exist(
        self,
        customer_repo: CustomerRepo,
        sample_customer_details: CustomerDetails,
        sample_customer_account: CustomerAccount,
    ):
        assert customer_repo.check_account_exist(sample_customer_account) is False

        customer_repo.create_customer(sample_customer_details)
        assert customer_repo.check_account_exist(sample_customer_account) is True

        # Different phone number
        different_phone = CustomerAccount(
            email=sample_customer_details.email, phone_number="+6511112222"
        )
        assert customer_repo.check_account_exist(different_phone) is False

        # Different email
        different_email = CustomerAccount(
            email="other@example.com", phone_number=sample_customer_details.phone_number
        )
        assert customer_repo.check_account_exist(different_email) is False

    def test_get_customer_details_when_not_found(self, customer_repo: CustomerRepo):
        details = customer_repo.get_customer_details("non-existent-sub")
        assert details == {
            "cust_id": "non-existent-sub",
            "cust_name": None,
            "last_login": None,
        }

    def test_get_customer_details_when_found_with_orders(
        self,
        customer_repo: CustomerRepo,
        sample_customer_details: CustomerDetails,
        in_memory_engine,
    ):
        created = customer_repo.create_customer(sample_customer_details)
        initial_login = created.f_last_login

        # Insert past orders for this customer
        order1 = CustomerOrders(
            f_order_id=10,
            f_cust_sub=sample_customer_details.customer_sub,
            f_dish_id=1,
            f_dish_name="Chicken Rice",
            f_quantity=2,
            f_order_price=10.0,
            f_order_status="COMPLETED",
        )
        order2 = CustomerOrders(
            f_order_id=10,
            f_cust_sub=sample_customer_details.customer_sub,
            f_dish_id=2,
            f_dish_name="Lime Juice",
            f_quantity=1,
            f_order_price=2.0,
            f_order_status="COMPLETED",
        )
        with Session(in_memory_engine) as session:
            session.add(order1)
            session.add(order2)
            session.commit()

        details = customer_repo.get_customer_details(sample_customer_details.customer_sub)

        expected_name = f"{sample_customer_details.first_name} {sample_customer_details.last_name}"
        assert details["cust_name"] == expected_name
        assert details["last_login"] == initial_login.strftime("%Y-%m-%d %H:%M:%S")
        assert len(details["past_orders"]["orders"]) == 2
        dish_names = [o["dish_name"] for o in details["past_orders"]["orders"]]
        assert "Chicken Rice" in dish_names
        assert "Lime Juice" in dish_names

        # Verify last_login was updated in database
        updated_cust = customer_repo.get_customer_by_email(sample_customer_details.email)
        assert updated_cust.f_last_login >= initial_login

    def test_update_customer_found(
        self, customer_repo: CustomerRepo, sample_customer_details: CustomerDetails
    ):
        customer_repo.create_customer(sample_customer_details)

        update_payload = CustomerDetails(
            first_name="Janet",
            last_name="Tan-Smith",
            email=sample_customer_details.email,
            phone_number="+6599998888",
            customer_sub=sample_customer_details.customer_sub,
        )
        updated = customer_repo.update_customer(update_payload)

        assert updated is not None
        assert updated.f_first_name == "Janet"
        assert updated.f_last_name == "Tan-Smith"
        assert updated.f_phone_number == "+6599998888"

    def test_update_customer_not_found(self, customer_repo: CustomerRepo):
        update_payload = CustomerDetails(
            first_name="Ghost",
            last_name="User",
            email="ghost@example.com",
            phone_number="+6500000000",
            customer_sub="ghost-sub",
        )
        result = customer_repo.update_customer(update_payload)
        assert result is None

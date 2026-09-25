from sqlalchemy import Engine
from sqlmodel import Session, select

from entities.customer_orders import CustomerOrders
from models.customer_order_details import CustomerOrderDetails


class CustomerOrdersRepo:
    def __init__(self, engine: Engine):
        self._engine = engine

    def update_cust_order(self, cust_order_details: CustomerOrderDetails):
        with Session(self._engine) as session:
            # 1. Fetch existing orders matching the customer and order ID
            statement = select(CustomerOrders).where(
                (CustomerOrders.f_cust_sub == cust_order_details.cust_sub) &
                (CustomerOrders.f_order_id == cust_order_details.order_id)
            )
            existing_orders = session.exec(statement).all()

            # 2. Process logic based on whether records exist
            if existing_orders:
                # Map incoming dishes by dish_id for O(1) instant lookup complexity
                incoming_dish_ids = {
                    d.dish_id
                    for o in cust_order_details.orders
                    for d in o.dishes
                }

                # Efficient update loop: O(N) linear time complexity
                for od in existing_orders:
                    if od.f_dish_id in incoming_dish_ids:
                        od.f_order_status = cust_order_details.status

                final_orders = existing_orders
            else:
                # Create new order rows if none existed
                final_orders = []
                for o in cust_order_details.orders:
                    for d in o.dishes:
                        final_orders.append(
                            CustomerOrders(
                                f_cust_sub=cust_order_details.cust_sub,
                                f_order_id=cust_order_details.order_id,
                                f_order_status=cust_order_details.status,
                                f_dish_id=d.dish_id,
                                f_dish_name=d.dish_name,
                                f_quantity=d.quantity,
                                f_order_price=d.price,
                                # Let your DB default handle f_order_date or pass it here
                            )
                        )
                session.add_all(final_orders)

            # 3. Save to database
            session.commit()

            # 4. Refresh elements to sync database state before serialization
            for order in final_orders:
                session.refresh(order)

            # 5. Build response list
            return [
                {
                    "order_id": order.f_order_id,
                    "order_status": order.f_order_status,
                    "dish_name": order.f_dish_name,
                    "quantity": order.f_quantity,
                    "order_price": order.f_order_price,
                    "order_date": order.f_order_date.isoformat() if order.f_order_date else None
                } for order in final_orders
            ]

    def _populate_cust_order(self, cust_order_details: CustomerOrderDetails) -> list[CustomerOrders]:
        order_list = []
        for o in cust_order_details.orders:
            for d in o.dishes:
                order_list.append(
                    CustomerOrders(
                        f_order_id=cust_order_details.order_id,
                        f_cust_sub=cust_order_details.cust_sub,
                        f_dish_id=d.dish_id,
                        f_dish_name=d.dish_name,
                        f_quantity=d.quantity,
                        f_order_price=d.price,
                        f_order_status=cust_order_details.status
                    )
                )

        return order_list
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from models.customer_details import CustomerDetails
from models.customer_account import CustomerAccount
from models.customer_order_details import CustomerOrderDetails
from user_service.user_service import UserService

cust_router = APIRouter(prefix="/v1/customer")


def get_user_service(request: Request):
    return request.app.state.user_service


@cust_router.post("/register")
async def register_user(
        customer_details: CustomerDetails,
        user_service: Annotated[UserService, None] = Depends(get_user_service)
):

    customer = user_service.register_customer(customer_details)
    return JSONResponse(
        content={
            "cust_id": customer.f_id,
            "cust_name": customer.f_first_name + " " + customer.f_last_name,
            "created_at": customer.f_created_at.isoformat()
        }
    )


@cust_router.post('/check_account_exist')
async def check_account_exist(
        customer_account: CustomerAccount,
        user_service: Annotated[UserService, None] = Depends(get_user_service)
):
    return JSONResponse(
        status_code=200,
        content={
            "account_exist": user_service.check_account_exist(customer_account)
        }
    )

@cust_router.get('/user/{cust_sub}')
async def get_user_details(
        cust_sub: str,
        user_service: Annotated[UserService, None] = Depends(get_user_service)
):
    customer = user_service.get_customer_details(cust_sub)
    return JSONResponse(
        content={
            **customer
        }
    )

@cust_router.post('/user/update_order')
async def update_order(
        order_details: CustomerOrderDetails,
        user_service: Annotated[UserService, None] = Depends(get_user_service)
):
    cust = user_service.update_cust_order(order_details)
    return JSONResponse(
        status_code=200,
        content={
            "message": "Customer Order Updated",

        }
    )

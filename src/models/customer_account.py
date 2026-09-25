from pydantic import BaseModel, EmailStr


class CustomerAccount(BaseModel):
    phone_number: str
    email: EmailStr

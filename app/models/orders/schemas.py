from pydantic import BaseModel, EmailStr, Field


class OrderInput(BaseModel):
    customer_name: str = Field(min_length=1)
    email: EmailStr
    delivery_address: str = Field(min_length=1)

from pydantic import BaseModel, EmailStr, Field


class CartItemInput(BaseModel):
    product_id: int
    quantity: int


class CartQuantityInput(BaseModel):
    quantity: int


class OrderInput(BaseModel):
    customer_name: str = Field(min_length=1)
    email: EmailStr
    delivery_address: str = Field(min_length=1)

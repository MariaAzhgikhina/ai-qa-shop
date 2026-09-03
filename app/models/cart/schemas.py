from pydantic import BaseModel


class CartItemInput(BaseModel):
    product_id: int
    quantity: int


class CartQuantityInput(BaseModel):
    quantity: int

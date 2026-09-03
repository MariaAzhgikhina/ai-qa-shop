from fastapi import APIRouter, Request, Response, status

from app.api.dependencies import db_path
from app.models.cart.schemas import CartItemInput, CartQuantityInput
from app.services.cart import service as cart_service


router = APIRouter(prefix="/cart", tags=["cart"])


@router.get("")
def get_cart(request: Request):
    return cart_service.cart_details(db_path(request), request.session.get("cart", {}))


@router.post("/items", status_code=status.HTTP_201_CREATED)
def add_cart_item(request: Request, item: CartItemInput):
    request.session["cart"] = cart_service.set_item(
        db_path(request), request.session.get("cart", {}), item.product_id, item.quantity, add=True
    )
    return cart_service.cart_details(db_path(request), request.session["cart"])


@router.patch("/items/{product_id}")
def update_cart_item(request: Request, product_id: int, item: CartQuantityInput):
    request.session["cart"] = cart_service.set_item(
        db_path(request), request.session.get("cart", {}), product_id, item.quantity
    )
    return cart_service.cart_details(db_path(request), request.session["cart"])


@router.delete("/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(request: Request, product_id: int):
    request.session["cart"] = cart_service.remove_item(request.session.get("cart", {}), product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

from fastapi import APIRouter, Request, Response, status

from app.models.schemas import CartItemInput, CartQuantityInput, OrderInput
from app.services import cart as cart_service
from app.services import catalog, orders


router = APIRouter(prefix="/api")


def db_path(request: Request) -> str:
    return request.app.state.db_path


@router.get("/products")
def products(request: Request, category: str | None = None, sort: str | None = None):
    return catalog.list_products(db_path(request), category, sort)


@router.get("/products/{product_id}")
def product(request: Request, product_id: int):
    return catalog.get_product(db_path(request), product_id)


@router.get("/cart")
def get_cart(request: Request):
    return cart_service.cart_details(db_path(request), request.session.get("cart", {}))


@router.post("/cart/items", status_code=status.HTTP_201_CREATED)
def add_cart_item(request: Request, item: CartItemInput):
    request.session["cart"] = cart_service.set_item(
        db_path(request), request.session.get("cart", {}), item.product_id, item.quantity, add=True
    )
    return cart_service.cart_details(db_path(request), request.session["cart"])


@router.patch("/cart/items/{product_id}")
def update_cart_item(request: Request, product_id: int, item: CartQuantityInput):
    request.session["cart"] = cart_service.set_item(
        db_path(request), request.session.get("cart", {}), product_id, item.quantity
    )
    return cart_service.cart_details(db_path(request), request.session["cart"])


@router.delete("/cart/items/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item(request: Request, product_id: int):
    request.session["cart"] = cart_service.remove_item(request.session.get("cart", {}), product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(request: Request, data: OrderInput):
    order = orders.create_order(
        db_path(request), request.session.get("cart", {}), data.customer_name, data.email, data.delivery_address
    )
    request.session["cart"] = {}
    return order


@router.get("/orders/{order_id}")
def order(request: Request, order_id: int):
    return orders.get_order(db_path(request), order_id)

from fastapi import APIRouter, Request, status

from app.api.dependencies import db_path
from app.models.orders.schemas import OrderInput
from app.services.orders import service as order_service


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_order(request: Request, data: OrderInput):
    order = order_service.create_order(
        db_path(request), request.session.get("cart", {}), data.customer_name, data.email, data.delivery_address
    )
    request.session["cart"] = {}
    return order


@router.get("/{order_id}")
def order(request: Request, order_id: int):
    return order_service.get_order(db_path(request), order_id)

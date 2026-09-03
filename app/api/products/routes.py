from fastapi import APIRouter, Request

from app.api.dependencies import db_path
from app.services.products import service as product_service


router = APIRouter(prefix="/products", tags=["products"])


@router.get("")
def products(request: Request, category: str | None = None, sort: str | None = None):
    return product_service.list_products(db_path(request), category, sort)


@router.get("/{product_id}")
def product(request: Request, product_id: int):
    return product_service.get_product(db_path(request), product_id)

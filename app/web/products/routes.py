from fastapi import APIRouter, Request

from app.errors import ShopError
from app.services.products import service as product_service
from app.web.shared import page_context, templates


router = APIRouter()


@router.get("/")
def catalog_page(request: Request, category: str | None = None, sort: str | None = None):
    products = product_service.list_products(request.app.state.db_path, category, sort)
    return templates.TemplateResponse(
        request,
        "products/catalog.html",
        page_context(
            request,
            products=products,
            categories=product_service.list_categories(request.app.state.db_path),
            selected_category=category or "",
            selected_sort=sort or "",
        ),
    )


@router.get("/products/{product_id}")
def product_page(request: Request, product_id: int):
    try:
        product = product_service.get_product(request.app.state.db_path, product_id)
    except ShopError as error:
        return templates.TemplateResponse(
            request,
            "shared/message.html",
            page_context(request, title="Product not found", message=error.message),
            status_code=404,
        )
    return templates.TemplateResponse(
        request, "products/product.html", page_context(request, product=product)
    )

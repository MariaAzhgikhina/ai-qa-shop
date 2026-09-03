from urllib.parse import quote

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from app.errors import ShopError
from app.services.cart import service as cart_service
from app.web.shared import page_context, templates


router = APIRouter()


@router.post("/cart/items")
def add_cart_item(request: Request, product_id: int = Form(...), quantity: int = Form(...)):
    try:
        request.session["cart"] = cart_service.set_item(
            request.app.state.db_path, request.session.get("cart", {}), product_id, quantity, add=True
        )
    except ShopError as error:
        return RedirectResponse(f"/products/{product_id}?error={quote(error.message)}", status_code=303)
    return RedirectResponse("/cart", status_code=303)


@router.get("/cart")
def cart_page(request: Request):
    details = cart_service.cart_details(request.app.state.db_path, request.session.get("cart", {}))
    return templates.TemplateResponse(request, "cart/cart.html", page_context(request, cart=details))


@router.post("/cart/items/{product_id}")
def update_cart_item(request: Request, product_id: int, quantity: int = Form(...)):
    try:
        request.session["cart"] = cart_service.set_item(
            request.app.state.db_path, request.session.get("cart", {}), product_id, quantity
        )
        return RedirectResponse("/cart", status_code=303)
    except ShopError as error:
        return RedirectResponse(f"/cart?error={quote(error.message)}", status_code=303)


@router.post("/cart/items/{product_id}/delete")
def delete_cart_item(request: Request, product_id: int):
    request.session["cart"] = cart_service.remove_item(request.session.get("cart", {}), product_id)
    return RedirectResponse("/cart", status_code=303)

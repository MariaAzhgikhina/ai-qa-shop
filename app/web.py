from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr, TypeAdapter, ValidationError

from app.errors import ShopError
from app.services import cart as cart_service
from app.services import catalog, orders


router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")


def page_context(request: Request, **values) -> dict:
    cart = request.session.get("cart", {})
    return {"request": request, "cart_count": sum(int(value) for value in cart.values()), **values}


@router.get("/")
def catalog_page(request: Request, category: str | None = None, sort: str | None = None):
    products = catalog.list_products(request.app.state.db_path, category, sort)
    return templates.TemplateResponse(
        request,
        "catalog.html",
        page_context(
            request,
            products=products,
            categories=catalog.list_categories(request.app.state.db_path),
            selected_category=category or "",
            selected_sort=sort or "",
        ),
    )


@router.get("/products/{product_id}")
def product_page(request: Request, product_id: int):
    try:
        product = catalog.get_product(request.app.state.db_path, product_id)
    except ShopError as error:
        return templates.TemplateResponse(
            request, "message.html", page_context(request, title="Product not found", message=error.message), status_code=404
        )
    return templates.TemplateResponse(request, "product.html", page_context(request, product=product))


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
    return templates.TemplateResponse(request, "cart.html", page_context(request, cart=details))


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


@router.get("/checkout")
def checkout_page(request: Request):
    details = cart_service.cart_details(request.app.state.db_path, request.session.get("cart", {}))
    if not details["items"]:
        return RedirectResponse("/cart?error=Your+cart+is+empty", status_code=303)
    return templates.TemplateResponse(request, "checkout.html", page_context(request, cart=details, error=None, values={}))


@router.post("/checkout")
def submit_checkout(
    request: Request,
    customer_name: str = Form(...),
    email: str = Form(...),
    delivery_address: str = Form(...),
):
    values = {"customer_name": customer_name, "email": email, "delivery_address": delivery_address}
    details = cart_service.cart_details(request.app.state.db_path, request.session.get("cart", {}))
    try:
        valid_email = str(TypeAdapter(EmailStr).validate_python(email))
        order = orders.create_order(
            request.app.state.db_path,
            request.session.get("cart", {}),
            customer_name,
            valid_email,
            delivery_address,
        )
    except ValidationError:
        return templates.TemplateResponse(
            request, "checkout.html", page_context(request, cart=details, error="Enter a valid email address", values=values), status_code=422
        )
    except ShopError as error:
        return templates.TemplateResponse(
            request, "checkout.html", page_context(request, cart=details, error=error.message, values=values), status_code=error.status_code
        )
    request.session["cart"] = {}
    return RedirectResponse(f"/orders/{order['id']}/confirmation", status_code=303)


@router.get("/orders/{order_id}/confirmation")
def confirmation_page(request: Request, order_id: int):
    try:
        order = orders.get_order(request.app.state.db_path, order_id)
    except ShopError as error:
        return templates.TemplateResponse(
            request, "message.html", page_context(request, title="Order not found", message=error.message), status_code=404
        )
    return templates.TemplateResponse(request, "confirmation.html", page_context(request, order=order))

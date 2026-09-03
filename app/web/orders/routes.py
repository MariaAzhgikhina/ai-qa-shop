from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from pydantic import EmailStr, TypeAdapter, ValidationError

from app.errors import ShopError
from app.services.cart import service as cart_service
from app.services.orders import service as order_service
from app.web.shared import page_context, templates


router = APIRouter()


@router.get("/checkout")
def checkout_page(request: Request):
    details = cart_service.cart_details(request.app.state.db_path, request.session.get("cart", {}))
    if not details["items"]:
        return RedirectResponse("/cart?error=Your+cart+is+empty", status_code=303)
    return templates.TemplateResponse(
        request, "orders/checkout.html", page_context(request, cart=details, error=None, values={})
    )


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
        order = order_service.create_order(
            request.app.state.db_path,
            request.session.get("cart", {}),
            customer_name,
            valid_email,
            delivery_address,
        )
    except ValidationError:
        return templates.TemplateResponse(
            request,
            "orders/checkout.html",
            page_context(request, cart=details, error="Enter a valid email address", values=values),
            status_code=422,
        )
    except ShopError as error:
        return templates.TemplateResponse(
            request,
            "orders/checkout.html",
            page_context(request, cart=details, error=error.message, values=values),
            status_code=error.status_code,
        )
    request.session["cart"] = {}
    return RedirectResponse(f"/orders/{order['id']}/confirmation", status_code=303)


@router.get("/orders/{order_id}/confirmation")
def confirmation_page(request: Request, order_id: int):
    try:
        order = order_service.get_order(request.app.state.db_path, order_id)
    except ShopError as error:
        return templates.TemplateResponse(
            request,
            "shared/message.html",
            page_context(request, title="Order not found", message=error.message),
            status_code=404,
        )
    return templates.TemplateResponse(
        request, "orders/confirmation.html", page_context(request, order=order)
    )

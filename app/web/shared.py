from pathlib import Path

from fastapi import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "templates")


def page_context(request: Request, **values) -> dict:
    cart = request.session.get("cart", {})
    return {"request": request, "cart_count": sum(int(value) for value in cart.values()), **values}

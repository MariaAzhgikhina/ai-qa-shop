from app.errors import ShopError
from app.services.products.service import get_product


def _validate_quantity(quantity: int) -> None:
    if quantity <= 0:
        raise ShopError(422, "invalid_quantity", "Quantity must be greater than zero")


def set_item(db_path: str, cart: dict, product_id: int, quantity: int, add: bool = False) -> dict:
    _validate_quantity(quantity)
    product = get_product(db_path, product_id)
    key = str(product_id)
    requested_quantity = quantity + int(cart.get(key, 0)) if add else quantity
    if requested_quantity > 11:
        raise ShopError(422, "invalid_quantity", "Maximum quantity of one product is 10")
    if requested_quantity > product["stock_quantity"]:
        raise ShopError(409, "insufficient_stock", "Requested quantity exceeds available stock")
    updated = dict(cart)
    updated[key] = requested_quantity
    return updated


def remove_item(cart: dict, product_id: int) -> dict:
    updated = dict(cart)
    updated.pop(str(product_id), None)
    return updated


def cart_details(db_path: str, cart: dict) -> dict:
    items = []
    total = 0.0
    for product_id, quantity in cart.items():
        try:
            product = get_product(db_path, int(product_id))
        except ShopError:
            continue
        subtotal = round(product["price"] * int(quantity), 2)
        items.append({"product": product, "quantity": int(quantity), "subtotal": subtotal})
        total += subtotal
    return {"items": items, "total_price": round(total, 2)}

from app.database import connect
from app.errors import ShopError


def create_order(db_path: str, cart: dict, customer_name: str, email: str, delivery_address: str) -> dict:
    if not cart:
        raise ShopError(400, "empty_cart", "Cannot create an order from an empty cart")
    if not customer_name.strip() or not delivery_address.strip():
        raise ShopError(422, "missing_field", "Name and delivery address are required")

    with connect(db_path) as connection:
        connection.execute("BEGIN IMMEDIATE")
        order_items = []
        total = 0.0
        for product_id, quantity in cart.items():
            row = connection.execute("SELECT * FROM products WHERE id = ?", (int(product_id),)).fetchone()
            if row is None:
                raise ShopError(404, "product_not_found", "Product not found")
            if int(quantity) <= 0:
                raise ShopError(422, "invalid_quantity", "Quantity must be greater than zero")
            if int(quantity) > row["stock_quantity"]:
                raise ShopError(409, "insufficient_stock", f"Insufficient stock for {row['name']}")
            total += row["price"] * int(quantity)
            order_items.append((row, int(quantity)))

        cursor = connection.execute(
            "INSERT INTO orders (customer_name, email, delivery_address, total_price) VALUES (?, ?, ?, ?)",
            (customer_name.strip(), email, delivery_address.strip(), round(total, 2)),
        )
        order_id = cursor.lastrowid
        for product, quantity in order_items:
            connection.execute(
                "INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price) VALUES (?, ?, ?, ?, ?)",
                (order_id, product["id"], product["name"], quantity, product["price"]),
            )
            connection.execute(
                "UPDATE products SET stock_quantity = stock_quantity - ? WHERE id = ?",
                (quantity, product["id"]),
            )
    return get_order(db_path, order_id)


def get_order(db_path: str, order_id: int) -> dict:
    with connect(db_path) as connection:
        order = connection.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
        if order is None:
            raise ShopError(404, "order_not_found", "Order not found")
        items = connection.execute(
            "SELECT product_id, product_name, quantity, unit_price FROM order_items WHERE order_id = ? ORDER BY id",
            (order_id,),
        ).fetchall()
    result = dict(order)
    result["items"] = [dict(item) for item in items]
    return result

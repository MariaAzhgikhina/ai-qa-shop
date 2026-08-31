from app.database import connect
from app.errors import ShopError


def list_products(db_path: str, category: str | None = None, sort: str | None = None) -> list[dict]:
    query = "SELECT * FROM products"
    params: list[str] = []
    if category:
        query += " WHERE category = ?"
        params.append(category)
    if sort == "price_asc":
        query += " ORDER BY price ASC, id ASC"
    elif sort == "price_desc":
        query += " ORDER BY price DESC, id ASC"
    else:
        query += " ORDER BY id ASC"

    with connect(db_path) as connection:
        return [dict(row) for row in connection.execute(query, params).fetchall()]


def get_product(db_path: str, product_id: int) -> dict:
    with connect(db_path) as connection:
        row = connection.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if row is None:
        raise ShopError(404, "product_not_found", "Product not found")
    return dict(row)


def list_categories(db_path: str) -> list[str]:
    with connect(db_path) as connection:
        rows = connection.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    return [row[0] for row in rows]

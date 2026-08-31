import sqlite3
from pathlib import Path


SEED_PRODUCTS = [
    (1, "Wireless Headphones", "Comfortable over-ear headphones with clear sound.", 79.90, "Electronics", 8),
    (2, "Portable Speaker", "Compact Bluetooth speaker for home and travel.", 49.50, "Electronics", 6),
    (3, "Desk Lamp", "Adjustable warm-light lamp for a desk or bedside table.", 34.00, "Home", 12),
    (4, "Ceramic Mug", "Stoneware mug with a matte blue finish.", 14.90, "Home", 20),
    (5, "Python Testing Guide", "A practical introduction to testing Python applications.", 39.00, "Books", 10),
    (6, "Web Quality Handbook", "Techniques for reliable web application testing.", 44.50, "Books", 7),
    (7, "Canvas Backpack", "Lightweight backpack with a padded laptop sleeve.", 59.90, "Accessories", 5),
    (8, "USB-C Cable", "Durable two-metre charging and data cable.", 12.50, "Accessories", 15),
    (9, "Mechanical Keyboard", "Compact keyboard with tactile switches.", 99.00, "Electronics", 4),
]


def connect(db_path: str) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(db_path: str) -> None:
    if db_path != ":memory:":
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with connect(db_path) as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                price REAL NOT NULL CHECK (price >= 0),
                category TEXT NOT NULL,
                stock_quantity INTEGER NOT NULL CHECK (stock_quantity >= 0)
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                email TEXT NOT NULL,
                delivery_address TEXT NOT NULL,
                total_price REAL NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL REFERENCES orders(id),
                product_id INTEGER NOT NULL REFERENCES products(id),
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity > 0),
                unit_price REAL NOT NULL
            );
            """
        )
        count = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            connection.executemany(
                "INSERT INTO products (id, name, description, price, category, stock_quantity) VALUES (?, ?, ?, ?, ?, ?)",
                SEED_PRODUCTS,
            )

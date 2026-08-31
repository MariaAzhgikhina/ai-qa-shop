def test_get_product_list(client):
    response = client.get("/api/products")

    assert response.status_code == 200
    assert len(response.json()) == 9
    assert response.json()[0]["name"] == "Wireless Headphones"


def test_get_existing_product(client):
    response = client.get("/api/products/5")

    assert response.status_code == 200
    assert response.json()["category"] == "Books"
    assert response.json()["price"] == 39.0


def test_get_nonexistent_product(client):
    response = client.get("/api/products/999")

    assert response.status_code == 404
    assert response.json() == {
        "error": {"code": "product_not_found", "message": "Product not found"}
    }


def test_create_valid_order(client):
    cart_response = client.post("/api/cart/items", json={"product_id": 1, "quantity": 2})
    assert cart_response.status_code == 201

    response = client.post(
        "/api/orders",
        json={
            "customer_name": "Alex Smith",
            "email": "alex@example.com",
            "delivery_address": "10 Market Street",
        },
    )

    assert response.status_code == 201
    assert response.json()["id"] == 1
    assert response.json()["total_price"] == 159.8
    assert response.json()["items"][0]["quantity"] == 2
    assert client.get("/api/cart").json()["items"] == []


def test_reject_invalid_quantity(client):
    response = client.post("/api/cart/items", json={"product_id": 1, "quantity": 0})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_quantity"

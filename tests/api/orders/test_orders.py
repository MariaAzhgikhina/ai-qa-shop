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

def test_reject_invalid_quantity(client):
    response = client.post("/api/cart/items", json={"product_id": 1, "quantity": 0})

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_quantity"

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

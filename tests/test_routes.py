from unittest.mock import patch

def test_get_all_items_returns_seed_data(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    items = response.get_json()
    assert len(items) == 2
    assert items[0]["product_name"] == "Organic Almond Milk"
    assert items[1]["product_name"] == "Peanut Butter"

def test_get_item_by_id_found(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    item = response.get_json()
    assert item["id"] == 1
    assert item["product_name"] == "Organic Almond Milk"


def test_get_item_by_id_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_create_item_success(client):
    payload = {
        "product_name": "Oat Milk",
        "brands": "Oatly",
        "price": 3.99,
        "stock_quantity": 10,
    }
    response = client.post("/inventory", json=payload)
    assert response.status_code == 201
    item = response.get_json()
    assert item["product_name"] == "Oat Milk"
    assert item["id"] == 3

    get_response = client.get(f"/inventory/{item['id']}")
    assert get_response.status_code == 200


def test_create_item_missing_required_fields(client):
    response = client.post("/inventory", json={"product_name": "Oat Milk"})
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_create_item_no_body(client):
    response = client.post("/inventory")
    assert response.status_code == 400


def test_lookup_and_add_success(client):
    fake_api_data = {
        "product_name": "Nutella",
        "brands": "Ferrero",
        "ingredients_text": "Sugar, palm oil, hazelnuts",
        "barcode": "3017620422003",
    }
    with patch("app.openfoodfacts.fetch_by_barcode", return_value=fake_api_data):
        response = client.post(
            "/inventory/lookup/3017620422003",
            json={"price": 5.99, "stock_quantity": 8},
        )
    assert response.status_code == 201
    item = response.get_json()
    assert item["product_name"] == "Nutella"
    assert item["price"] == 5.99
    assert item["stock_quantity"] == 8


def test_lookup_and_add_not_found(client):
    with patch("app.openfoodfacts.fetch_by_barcode", return_value=None):
        response = client.post("/inventory/lookup/0000000000000")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_lookup_and_add_no_body_uses_defaults(client):
    fake_api_data = {
        "product_name": "Mystery Snack",
        "brands": "Unknown",
        "ingredients_text": "",
        "barcode": "1111111111111",
    }
    with patch("app.openfoodfacts.fetch_by_barcode", return_value=fake_api_data):
        response = client.post("/inventory/lookup/1111111111111") 
    assert response.status_code == 201
    item = response.get_json()
    assert item["price"] == 0.0
    assert item["stock_quantity"] == 0


def test_update_item_success(client):
    response = client.patch("/inventory/1", json={"price": 5.49, "stock_quantity": 25})
    assert response.status_code == 200
    item = response.get_json()
    assert item["price"] == 5.49
    assert item["stock_quantity"] == 25
    assert item["product_name"] == "Organic Almond Milk"


def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1.0})
    assert response.status_code == 404


def test_update_item_no_body(client):
    response = client.patch("/inventory/1")
    assert response.status_code == 400


def test_delete_item_success(client):
    response = client.delete("/inventory/2")
    assert response.status_code == 200
    deleted = response.get_json()
    assert deleted["id"] == 2

    get_response = client.get("/inventory/2")
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404


def test_delete_item_at_index_zero(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1

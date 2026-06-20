import pytest

def test_add_to_cart(authorized_client, product_for_test):
    response = authorized_client.post("/cart/", json = {
        "product_id": product_for_test,
        "quantity": 1
    })
    assert response.status_code == 200

def test_get_cart_empty(authorized_client):
    response = authorized_client.get("/cart/")
    data = response.json()
    assert len(data) == 0
    assert response.status_code == 200

def test_get_cart_with_items(authorized_client, product_for_test):
    authorized_client.post("/cart/", json = {
        "product_id": product_for_test,
        "quantity": 1
    })
    response = authorized_client.get("/cart/")
    data = response.json()
    assert len(data) == 1
    assert response.status_code == 200
    assert data[0]["title"] == "testproduct"
    assert data[0]["quantity"] == 1

def test_remove_from_cart(authorized_client, product_for_test):
    authorized_client.post("/cart/", json = {
        "product_id": product_for_test,
        "quantity": 1,
    })

    get = authorized_client.get("/cart/")
    data = get.json()

    item_id = data[0]["id"]

    response = authorized_client.delete(f"/cart/{item_id}/")  
    assert response.status_code == 200

    response_get = authorized_client.get("/cart/")
    assert response_get.status_code == 200
    response_get_data = response_get.json()
    assert len(response_get_data) == 0

def test_add_to_cart_unauthorized(client, product_for_test):
    response = client.post("/cart/", json = {
        "product_id": product_for_test,
        "quantity": 1
    })

    assert response.status_code == 401

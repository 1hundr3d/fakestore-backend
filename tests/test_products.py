import pytest

def test_get_products_empty(client):
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert data == []

def test_create_products(authorized_client):
    response = authorized_client.post("/products/", json={
        "title": "testtitle",
        "price": 1234.56,
        "description": "testdescription",
        "image": "image.url"
    })

    assert response.status_code == 200

    data = response.json()
    assert data["price"] == 1234.56
    
def test_create_product_unauthorized(client):
    response = client.post("/products/", json={
        "title": "testtitle",
        "price": 1234.56,
        "description": "testdescription",
        "image": "image.url"
    })

    assert response.status_code == 401

def test_get_products_with_data(authorized_client):
    authorized_client.post("/products/", json={
        "title": "testtitle",
        "price": 1234.56,
        "description": "testdescription",
        "image": "image.url"
    })

    response = authorized_client.get("/products/")
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "testtitle"
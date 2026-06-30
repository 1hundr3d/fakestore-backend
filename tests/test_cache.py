import pytest
from app.cache import delete_cache

def test_product_cache(authorized_client):
    delete_cache("products:list")
    authorized_client.get("/products/")
    new_product = authorized_client.post("/products/", json={
        "title": "testtitle",
        "price": 1234.56,
        "description": "testdescription",
        "image": "image.url"
    })
    product_json = new_product.json()
    response = authorized_client.get("/products/")
    response_json = response.json()

    assert len(response_json) >= 1
    assert response_json[0]["title"] == product_json["title"]
import pytest

def test_register_success(client):
    response = client.post("/auth/register", json={
        "username": "testuser1",
        "password": "testpassword1"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate(client):
    client.post("/auth/register", json={
        "username": "testuser2",
        "password": "testpassword2"
    })

    response = client.post("/auth/register", json={
        "username": "testuser2",
        "password": "testpassword2"
    })

    assert response.status_code == 400

def test_login(client):
    client.post("/auth/register", json={
        "username": "testuser3",
        "password": "testpassword3"
    })

    response = client.post("/auth/login", json={
        "username": "testuser3",
        "password": "testpassword3"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
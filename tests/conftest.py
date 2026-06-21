import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from fastapi.testclient import TestClient
from app.database import Base
from app.main import app
from app.database import get_db

from app.models import UserDB, Products, CartItem

TEST_DATABASE_URL = os.getenv(
    'TEST_DATABASE_URL',
    'sqlite:///./test.db'
)

@pytest.fixture(scope="session", autouse=True)
def create_test_db(engine):
    Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="session")
def engine():
    return create_engine(TEST_DATABASE_URL, poolclass = NullPool, connect_args={"check_same_thread": False})

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope='function')
def client(db_session):
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope='function')
def token(client, db_session):
    register_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    client.post("/auth/register", json=register_data)
    response = client.post("/auth/login", json=register_data)
    return response.json()["access_token"]

@pytest.fixture(scope='function')
def authorized_client(client, token):
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.fixture(scope='function')
def product_for_test(authorized_client):
    product_data = {
        "title": "testproduct",
        "price": 12345.123,
        "description": "testproduct",
        "image": "testproduct.url"
    }
    product = authorized_client.post("/products/", json = product_data)
    product_data_response = product.json()
    return product_data_response["id"]
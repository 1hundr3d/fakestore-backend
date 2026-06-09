from pydantic import BaseModel
from typing import Optional

# Пользовательские модели
class UserRegister(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class UserLogin(BaseModel):
    username: str
    password: str

# Модели для товаров
class ProductOut(BaseModel):
    id: int
    title: str
    price: float
    description: Optional[str] = None
    image: Optional[str] = None

    class Config:
        orm_mode = True

#Модели для корзины
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemOut(BaseModel):
    id: int
    title: str
    price: float
    quantity: int = 1
    image: Optional[str] = None
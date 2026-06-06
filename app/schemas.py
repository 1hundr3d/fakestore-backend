from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class UserLogin(BaseModel):
    login: str
    password: str


#IMPORTS
import os
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserDB

#CONSTANTS
SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey1234567890")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#HASHING PASSWORDS
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#hash
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
#verify
def verify_password(password: str, hashed_password:str) -> bool:
    return pwd_context.verify(password, hashed_password)

#JWT
def create_access_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

#Получаем нужного пользователя
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db) ) -> UserDB:

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code = 401, detail="Не удалось подтвердить данные")
    except JWTError:
        raise HTTPException(status_code=401, detail="Не удалось подтвердить данные")
    
    user = db.query(UserDB).filter(UserDB.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Не удалось подтвердить данные")
    return user

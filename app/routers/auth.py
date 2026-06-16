from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import UserDB
from app.schemas import UserRegister, UserLogin, Token
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model = Token)
async def register(user_data: UserRegister, db: Session=Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Имя пользователя занято")

    password = hash_password(user_data.password)
    new_user = UserDB(username=user_data.username, hashed_password=password)
    db.add(new_user)
    db.commit()

    access_token = create_access_token(new_user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model = Token)
async def login(user_data: UserLogin, db: Session=Depends(get_db)):
    existing_user = db.query(UserDB).filter(UserDB.username == user_data.username).first()
    if not existing_user or not verify_password(user_data.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail='Неверный логин или пароль')
    
    access_token = create_access_token(username = existing_user.username)
    return {"access_token": access_token, "token_type": "bearer"}
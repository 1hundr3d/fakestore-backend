from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Products, UserDB
from app.schemas import ProductOut, ProductCreate
from typing import Optional
from app.auth import get_current_user

router = APIRouter(prefix="/products", tags=["products"], redirect_slashes=False)

@router.get("/", response_model=list[ProductOut])
async def products(search: Optional[str] = None, db: Session=Depends(get_db)):
    if not search:
        all_products = db.query(Products).all()
        return all_products
    existing_search = db.query(Products).filter(Products.title.ilike(f"%{search}%")).all()
    return existing_search

@router.post("/", response_model=ProductOut)
async def create_product(product_data: ProductCreate, db: Session=Depends(get_db), current_user: UserDB=Depends(get_current_user)):
    new_product = Products(title = product_data.title, price = product_data.price, description = product_data.description, image = product_data.image)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Products, UserDB
from app.schemas import ProductOut, ProductCreate
from typing import Optional
from app.auth import get_current_user
from app.cache import set_cache, get_cache, delete_cache

router = APIRouter(prefix="/products", tags=["products"], redirect_slashes=False)

@router.get("/", response_model=list[ProductOut])
async def products(search: Optional[str] = None, db: Session=Depends(get_db)):
    if search:
        return db.query(Products).filter(Products.title.ilike(f"%{search}%")).all()
    
    if not search:
        cached = get_cache("products:list")
        if cached is not None:
            return cached
        all_products = db.query(Products).all()
        set_cache("products:list", all_products, ttl=300)
        return all_products

@router.post("/", response_model=ProductOut)
async def create_product(product_data: ProductCreate, db: Session=Depends(get_db), current_user: UserDB=Depends(get_current_user)):
    new_product = Products(title = product_data.title, price = product_data.price, description = product_data.description, image = product_data.image)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    delete_cache("products:list")
    return new_product
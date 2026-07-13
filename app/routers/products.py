from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Products, UserDB
from app.schemas import ProductOut, ProductCreate
from typing import Optional
from app.auth import get_current_user
from app.cache import set_cache, get_cache, delete_cache

from app.discounts.strategies import NoDiscount, SeasonalDiscount

from app.observers import ProductSubject, LoggerObserver, EmailObserver

product_subject = ProductSubject()
product_subject.attach(LoggerObserver)
product_subject.attach(EmailObserver)

router = APIRouter(prefix="/products", tags=["products"], redirect_slashes=False)

discount_strategy = SeasonalDiscount({12: 0.15, 1: 0.10})
# discount_strategy = NoDiscount

@router.get("/", response_model=list[ProductOut])
async def products(search: Optional[str] = None, db: Session=Depends(get_db)):
    if search:
        return db.query(Products).filter(Products.title.ilike(f"%{search}%")).all()
    
    if not search:
        cached = get_cache("products:list")

        if cached is not None:
            discounted_products = []
            for item in cached:
                new_item = item.copy()
                new_price = discount_strategy.apply(item["price"])
                new_item["price"] = new_price
                discounted_products.append(new_item)
            return discounted_products

        all_products = db.query(Products).all()

        result = []
        for p in all_products:
            result.append({
                "id": p.id,
                "title": p.title,
                "price": discount_strategy.apply(p.price),
                "description": p.description,
                "image": p.image
            })

        set_cache("products:list", result, ttl=300)
        return result

@router.post("/", response_model=ProductOut)
async def create_product(product_data: ProductCreate, db: Session=Depends(get_db), current_user: UserDB=Depends(get_current_user)):
    new_product = Products(title = product_data.title, price = product_data.price, description = product_data.description, image = product_data.image)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    delete_cache("products:list")
    product_subject.notify(f"Новый товар создан: {product_data.title}")
    return new_product
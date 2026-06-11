from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CartItem, Products
from app.schemas import CartItemCreate, CartItemOut
from app.auth import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"], redirect_slashes=False)

@router.get("/", response_model=list[CartItemOut])
async def get_cart(current_user: UserDB=Depends(get_current_user), db: Session=Depends(get_db)):
    all_items = db.query(CartItem).filter(CartItem.user_id == current_user.id).all()

    result = []
    for item in all_items:
        product = db.query(Products).filter(Products.id == item.product_id).first()
        result.append(CartItemOut(id = item.id, title = product.title, price = product.price, quantity = product.quantity, image = product.image))
    return result

@router.post("/")
async def add_cart(current_user: UserDB=Depends(get_current_user), db: Session=Depends(get_db), cart_data: CartItemCreate):
    if db.query(Products).filter(Products.id == cart_data.product_id).first() is None:
        raise HTTPException(status_code=404, detail='Товар не найден')
    existing_item = db.query(CartItem).filter(CartItem.user_id == current_user.id, CartItem.product_id == cart_data.product_id).first()
    if existing_item:
        existing_item.quantity += cart_data.quantity
        db.add(existing_item)
        db.commit()
    else:
        new_item = CartItem(user_id = current_user.id, product_id = cart_data.product_id, quantity = cart_data.quantity)
        db.add(new_item)
        db.commit()
    return {"status":"ok"}

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.entities import Item as ItemEntity
from app.models import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])


@router.get("", response_model=list[Item])
def get_items(db: Session = Depends(get_db)):
    return db.query(ItemEntity).all()


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemEntity).filter(ItemEntity.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    new_item = ItemEntity(name=item.name, price=item.price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(ItemEntity).filter(ItemEntity.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.price = item.price
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(ItemEntity).filter(ItemEntity.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(db_item)
    db.commit()
    return {"deleted": item_id}
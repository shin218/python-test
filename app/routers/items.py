# app/routers/items.py
from fastapi import APIRouter, HTTPException
from app.models import Item, ItemCreate
from app import database

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.post("", response_model=Item)
def create_item(item: ItemCreate):
    new_item = {"id": database.next_id, "name": item.name, "price": item.price}
    database.items_db[database.next_id] = new_item
    database.next_id += 1
    return new_item


@router.get("", response_model=list[Item])
def get_items():
    return list(database.items_db.values())


@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in database.items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return database.items_db[item_id]


@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    if item_id not in database.items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    database.items_db[item_id] = {"id": item_id, "name": item.name, "price": item.price}
    return database.items_db[item_id]


@router.delete("/{item_id}")
def delete_item(item_id: int):
    if item_id not in database.items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del database.items_db[item_id]
    return {"deleted": item_id}
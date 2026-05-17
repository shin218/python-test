from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id, "name": f"item-{item_id}"}

class Item(BaseModel):
    name: str
    price: float

@app.post("/items")
def create_item(item: Item):
    total = item.price * 1.1  # 부가세 10%
    return {"created": item, "total_with_tax": total}   
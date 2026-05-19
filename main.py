from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# FastAPI 애플리케이션 인스턴스 생성
# FastAPI app = new FastAPI() -> JAVA로 치면 이거랑 동일
app = FastAPI()

# 인메모리 저장소 (DB 대신 dict 사용)
items_db: dict[int, dict] = {}
next_id = 1


# 요청용 모델 (생성/수정 시)
class ItemCreate(BaseModel):
    name: str
    price: float


# 응답용 모델 (조회 시 id 포함)
class Item(BaseModel):
    id: int
    name: str
    price: float


@app.get("/")
def hello():
    return {"message": "Hello"}


@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    # global 키워드를 사용하여 전역 변수 next_id를 사용할 수 있게 함
    global next_id
    new_item = {"id": next_id, "name": item.name, "price": item.price}
    items_db[next_id] = new_item
    next_id += 1
    return new_item    


@app.get("/items", response_model=list[Item])
def get_items():
    return list(items_db.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


#@app -> 데코레이터(Decorator) -> 함수에 기능을 추가하는 역할(java의 어노테이션과 비슷함)
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = {"id": item_id, "name": item.name, "price": item.price}
    return items_db[item_id]


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"deleted": item_id}
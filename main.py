from fastapi import FastAPI

from app.database import Base, engine
from app.entities import Item
from app.routers import items, chat   # ← chat 추가

# 앱 시작 시 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)
app.include_router(chat.router)   # ← chat 라우터 등록 추가


@app.get("/")
def hello():
    return {"message": "Hello"}
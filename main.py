from fastapi import FastAPI

from app.database import Base, engine
from app.entities import Item
from app.routers import items, chat, documents, rag   # ← documents 추가
from app.services import qdrant_service               # ← 추가

# 앱 시작 시 SQL 테이블 자동 생성
Base.metadata.create_all(bind=engine)

# 앱 시작 시 Qdrant 컬렉션 자동 생성 ← 추가
qdrant_service.init_collection()

app = FastAPI()

app.include_router(items.router)
app.include_router(chat.router)
app.include_router(documents.router)   # ← 추가
app.include_router(rag.router)   # ← 추가


@app.get("/")
def hello():
    return {"message": "Hello"}
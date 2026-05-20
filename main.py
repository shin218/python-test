from fastapi import FastAPI

from app.database import Base, engine
from app.entities import Item  # 테이블 생성을 위해 import 필요
from app.routers import items

# 앱 시작 시 테이블 자동 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(items.router)


@app.get("/")
def hello():
    return {"message": "Hello"}
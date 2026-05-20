from pydantic import BaseModel


# 요청용 모델 (생성/수정 시)
class ItemCreate(BaseModel):
    name: str
    price: float


# 응답용 모델 (조회 시 id 포함)
class Item(BaseModel):
    id: int
    name: str
    price: float
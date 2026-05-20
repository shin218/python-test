from sqlalchemy import Column, Integer, String, Float

from app.database import Base

#DB 모델
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
from fastapi import APIRouter
from pydantic import BaseModel

from app.services import qdrant_service

router = APIRouter(prefix="/documents", tags=["documents"])


# 요청 모델
class DocumentAdd(BaseModel):
    id: int
    text: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


# 응답 모델
class SearchResult(BaseModel):
    id: int
    score: float
    text: str


@router.post("")
def add_document(doc: DocumentAdd):
    qdrant_service.add_document(doc.id, doc.text)
    return {"status": "added", "id": doc.id}


@router.post("/search", response_model=list[SearchResult])
def search_documents(request: SearchRequest):
    return qdrant_service.search_similar(request.query, request.top_k)
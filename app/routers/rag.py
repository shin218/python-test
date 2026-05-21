from fastapi import APIRouter
from pydantic import BaseModel

from app.services import rag_service

router = APIRouter(prefix="/rag", tags=["rag"])


# 요청 모델
class RagRequest(BaseModel):
    query: str
    top_k: int = 3


# 응답 모델
class SourceDocument(BaseModel):
    id: int
    score: float
    text: str


class RagResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]


@router.post("", response_model=RagResponse)
def answer(request: RagRequest):
    result = rag_service.answer_question(request.query, request.top_k)
    return result
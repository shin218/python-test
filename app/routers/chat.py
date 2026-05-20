from fastapi import APIRouter
from pydantic import BaseModel

from app.services import openai_service

router = APIRouter(prefix="/chat", tags=["chat"])


# 요청 모델
class ChatRequest(BaseModel):
    message: str


# 응답 모델
class ChatResponse(BaseModel):
    response: str


@router.post("", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = openai_service.chat(request.message)
    return ChatResponse(response=answer)
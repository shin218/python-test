from openai import OpenAI

from app.config import OPENAI_API_KEY

# OpenAI 클라이언트 (5일차에 만든 거랑 동일 패턴)
client = OpenAI(api_key=OPENAI_API_KEY)

# 임베딩 모델
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSION = 1536  # 이 모델의 벡터 차원


def create_embedding(text: str) -> list[float]:
    """
    텍스트를 받아서 임베딩 벡터로 변환.
    """
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding
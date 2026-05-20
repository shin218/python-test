from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from app.services.embedding_service import EMBEDDING_DIMENSION, create_embedding

# Qdrant 클라이언트 (REST 포트 사용)
client = QdrantClient(host="localhost", port=6333)

# 컬렉션 이름 (Spring에서 테이블 이름 같은 개념)
COLLECTION_NAME = "documents"


def init_collection():
    """
    컬렉션이 없으면 생성. 앱 시작 시 1번 호출.
    """
    # 컬렉션 이름 목록 가져오기(리스트 컴프리헨션)
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIMENSION,
                distance=Distance.COSINE,
            ),
        )


def add_document(doc_id: int, text: str):
    """
    텍스트를 임베딩하여 Qdrant에 저장.
    """
    vector = create_embedding(text)
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=doc_id,
                vector=vector,
                payload={"text": text},
            )
        ],
    )


def search_similar(query: str, top_k: int = 5) -> list[dict]:
    query_vector = create_embedding(query)
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    ).points
    return [
        {
            "id": hit.id,
            "score": hit.score,
            "text": hit.payload["text"],
        }
        for hit in results
    ]
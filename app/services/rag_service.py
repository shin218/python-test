from openai import OpenAI

from app.config import OPENAI_API_KEY
from app.services import qdrant_service

client = OpenAI(api_key=OPENAI_API_KEY)

CHAT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """당신은 주어진 문서를 기반으로 사용자 질문에 답하는 어시스턴트입니다.

규칙:
1. 반드시 제공된 문서 내용을 근거로 답변하세요.
2. 문서에 없는 내용은 추측하지 말고 "제공된 문서에서 해당 정보를 찾을 수 없습니다"라고 답하세요.
3. 답변은 간결하게 한국어로 작성하세요.
"""


def answer_question(query: str, top_k: int = 3) -> dict:
    """
    질문을 받아서:
    1. 유사 문서 검색
    2. 문서를 컨텍스트로 LLM에 전달
    3. 답변 생성
    """
    # 1. 유사 문서 검색
    search_results = qdrant_service.search_similar(query, top_k)

    # 2. 검색 결과를 컨텍스트 문자열로 변환
    context = "\n\n".join([
        f"[문서 {i+1}] {result['text']}"
        for i, result in enumerate(search_results)
    ])

    # 3. LLM 호출
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"참고 문서:\n{context}\n\n질문: {query}"},
        ],
    )

    answer = response.choices[0].message.content

    # 4. 답변 + 참고한 문서들을 같이 반환
    return {
        "answer": answer,
        "sources": search_results,
    }
from openai import OpenAI

from app.config import OPENAI_API_KEY

# OpenAI 클라이언트 생성 (전역 1개 재사용)
client = OpenAI(api_key=OPENAI_API_KEY)


def chat(user_message: str) -> str:
    """
    사용자 메시지를 받아서 OpenAI 응답을 반환.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": user_message}
        ],
    )
    return response.choices[0].message.content
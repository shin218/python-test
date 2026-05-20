import os
from dotenv import load_dotenv

# .env 파일을 읽어서 환경변수에 로드
load_dotenv()

# 환경변수에서 값 읽기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API 키 누락 시 명확한 에러
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY가 설정되지 않았습니다. "
        ".env 파일에 OPENAI_API_KEY=sk-... 형식으로 추가해주세요."
    )
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. DB 연결 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 전용 설정
)

# 2. 세션 팩토리 (Spring의 EntityManagerFactory 비슷)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3. Entity 부모 클래스 (Spring의 @Entity 베이스)
Base = declarative_base()


# 4. DI용 함수 (FastAPI의 Depends에서 호출)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
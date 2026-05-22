# Java/Spring Boot vs Python/FastAPI: RAG 챗봇 포팅 비교

> 동일한 RAG 챗봇을 **Java/Spring Boot**로 먼저 구현한 뒤 **Python/FastAPI**로 포팅한 학습 프로젝트의 비교 문서입니다.

- Java 원본: [shin218/rag-chatbot](https://github.com/shin218/rag-chatbot)
- Python 포팅: [shin218/python-test](https://github.com/shin218/python-test)

---

## 1. 포팅 배경

Java/Spring 백엔드 경력자가 **AI/LLM 백엔드로 직무 전환**을 준비하면서, Python 생태계의 RAG 구현 패턴을 익히기 위해 진행한 포팅 작업입니다.

원본 Java 버전에서 이미 비즈니스 로직·아키텍처·실험 기반 의사결정을 완료했기 때문에, Python 포팅 시 **순수하게 언어/프레임워크 차이에만 집중**할 수 있었습니다.

**개발 기간 비교**

| 구분 | Java 원본 | Python 포팅 |
|------|----------|------------|
| 학습 + 구현 | 수 주 (실험·튜닝 포함) | **8일** (학습 + 구현 + 문서화) |

Python 포팅이 빨랐던 이유는 본인의 Python 학습 속도가 아니라, **이미 Java로 한 번 만들어본 RAG 구조를 그대로 이식한 것**이기 때문입니다. 비즈니스 고민을 다시 할 필요가 없었습니다.

---

## 2. 한눈에 비교

| 항목 | Java/Spring Boot | Python/FastAPI |
|------|-----------------|----------------|
| **언어** | Java 17 | Python 3.12 |
| **프레임워크** | Spring Boot | FastAPI |
| **빌드 도구** | Gradle | pip + requirements.txt |
| **DI 방식** | `@Autowired` (클래스 멤버) | `Depends(get_db)` (함수 인자) |
| **벡터 DB** | Qdrant (REST 직접 구현) | Qdrant (qdrant-client SDK) |
| **임베딩 모델** | text-embedding-3-small (1536) | text-embedding-3-small (1536) |
| **LLM** | gpt-4o-mini | gpt-4o-mini |
| **검색 방식** | **Dense + Sparse Hybrid (RRF)** | Dense only |
| **청크 전략** | **500자 (실험 기반 채택)** | 미적용 (문서 단위 1벡터) |
| **PDF 처리** | PDFBox + Vision 표 추출 | 미구현 |
| **평가 검증** | **Hit@3, score, 노이즈 수동 측정** | 시나리오 기반 동작 검증 |

진하게 표시한 항목은 Java 버전이 더 깊이 들어간 부분입니다. Python 포팅은 의도적으로 단순화했습니다 (시간 제약 + 학습 우선순위).

---

## 3. 프레임워크 차이 체감 포인트

### 3.1 의존성 주입 (DI)

**Spring (클래스 멤버 주입)**

```java
@RestController
@RequestMapping("/items")
public class ItemController {
    @Autowired
    private SessionFactory sessionFactory;
    
    @GetMapping
    public List<Item> getItems() {
        Session db = sessionFactory.openSession();
        try { ... } 
        finally { db.close(); }
    }
}
```

**FastAPI (함수 인자 주입)**

```python
@router.get("")
def get_items(db: Session = Depends(get_db)):
    return db.query(ItemEntity).all()
```

**체감 차이**: FastAPI 방식이 더 명시적입니다. "이 함수는 db에 의존한다"가 시그니처에 보이고, 자원 정리(`db.close()`)는 `get_db()`의 `yield` 패턴이 자동 처리합니다.

### 3.2 ORM 동작

**Spring JPA**: `@Transactional`이 자동 커밋, dirty checking으로 자동 UPDATE

**SQLAlchemy**: 모든 변경에 명시적 `db.commit()`, `db.refresh()` 필요

처음엔 SQLAlchemy의 명시성이 번거롭게 느껴졌지만, **"내가 컨트롤한다"는 감각**이 디버깅에 도움됐습니다.

### 3.3 코드 분량

동일 기능 기준으로 Python이 짧습니다.

| 비교 항목 | Java | Python |
|----------|------|--------|
| Entity 정의 | `@Entity` + `@Table` + 필드 + 어노테이션 | `class Item(Base)` + `Column` 정의 |
| DTO | Lombok `@Data` 또는 record | Pydantic `BaseModel` 상속 |
| Validation | `@Valid` + Bean Validation 어노테이션 | Pydantic이 자동 |
| Swagger 문서 | SpringDoc 설정 필요 | FastAPI 기본 내장 (`/docs`) |

**구체 예**: DTO + Validation + JSON 직렬화를 Java에선 Lombok + Bean Validation + Jackson 조합으로 처리하는 것을, Python에선 Pydantic `BaseModel` 상속 한 줄로 끝낼 수 있습니다.

### 3.4 환경 격리

| | Java | Python |
|---|------|--------|
| 의존성 격리 | Gradle/Maven이 자동 (`build/`, `.gradle/`) | venv 명시적으로 만들어야 함 |
| 버전 충돌 | 빌드 도구가 자동 해결 | venv 활성화 안 하면 시스템 Python에 설치되어 충돌 발생 |

Python의 가상환경은 **명시적이라 깔끔하지만, 깜빡하면 디버깅하기 어려운 함정**이 됨. 실제로 포팅 중 venv 활성화 누락으로 한 차례 디버깅을 했습니다.

---

## 4. 의도적으로 단순화한 부분

Python 포팅에서 **Java 버전 대비 줄인 기능**들. 모두 시간 제약 + 학습 우선순위 판단이며, 한계로 인지하고 있습니다.

| 영역 | Java | Python | 비고 |
|------|------|--------|------|
| **청크 분할** | 500자, 실험 기반 | 없음 | 학습 단순화 |
| **Hybrid 검색** | Dense + Sparse + RRF | Dense only | 우선순위 낮춰 |
| **PDF 파싱** | PDFBox + Vision 표 추출 | 미구현 | 학습 범위 외 |
| **평가 검증** | Hit@3, score 수동 측정 | 시나리오 동작 검증만 | 평가셋 부재 |

이 부분들은 [Python README의 한계 섹션](https://github.com/shin218/python-test#9-한계-및-개선-방향)에 명시했으며, 다음 학습 단계의 과제입니다.

---

## 5. Java 경험이 Python 학습을 가속한 부분

본인이 Java/Spring 베이스를 가진 상태에서 Python을 학습할 때, **개념 매핑이 거의 1:1**로 가능했던 점이 학습 속도를 크게 단축했습니다.

| Spring 개념 | FastAPI 대응 | 학습 시간 |
|------------|-------------|----------|
| `@RestController` + `@RequestMapping` | `APIRouter(prefix="/...")` | 10분 |
| `@GetMapping`, `@PostMapping` | `@router.get`, `@router.post` | 5분 |
| `@PathVariable` | 함수 파라미터 (자동) | 즉시 |
| `@RequestBody` + DTO | Pydantic `BaseModel` | 30분 |
| `@Autowired` | `Depends(...)` | 30분 |
| `@Entity`, JPA Repository | SQLAlchemy `Base` + Session | 1시간 |
| `application.yml` + `@Value` | `.env` + `os.getenv` | 20분 |

**가장 빨랐던 부분**: HTTP 라우팅, DTO 정의 (이미 패턴을 알고 있어서 문법만 매핑)

**가장 시간 든 부분**: SQLAlchemy의 명시적 commit/refresh 패턴, FastAPI의 `Depends` 함수형 DI 사고 전환

---

## 6. 어떤 상황에 어떤 스택을 쓸까

본인의 학습 과정에서 형성된 판단입니다. 절대적 기준은 아닙니다.

### Java/Spring Boot가 유리한 경우
- 대규모·장기 운영 백엔드 (정적 타입 안전성)
- 엔터프라이즈 환경 (Spring 생태계 성숙도)
- 팀 규모가 크고 코드 일관성 필요

### Python/FastAPI가 유리한 경우
- **AI/LLM 통합 백엔드 (라이브러리 풍부도 압도적)**
- 빠른 프로토타이핑·MVP
- 데이터 사이언스 파이프라인과 통합 필요

본인이 RAG 챗봇을 양쪽으로 만들어본 결과, **AI 기능 통합 영역에서는 Python 생태계의 우위가 명확**했습니다. OpenAI SDK, qdrant-client 모두 Python 버전이 먼저 나오고 더 활발히 업데이트됩니다.

---

## 7. 포팅으로 얻은 것

### 기술적 성과
- Java/Spring 베이스를 유지하면서 Python/FastAPI 기본 패턴 익힘
- 동일 문제를 두 언어로 해결한 비교 경험
- SQLAlchemy ORM, Pydantic, qdrant-client 등 Python 핵심 라이브러리 실사용

### 학습 방법론적 성과
- AI 도구(Cursor, Claude) 활용한 가속 학습 패턴 검증
- 게으른 사람의 학습 한계 극복 - "작은 단위 + 외부 의사결정 + 즉시 실행" 패턴

### 다음 학습 과제
- Python 버전에 청킹·Hybrid 검색 도입
- async/await로 동시성 개선
- 평가 자동화 (RAGAS 등)
- 두 버전의 성능·비용 비교 측정

---

*이 비교는 2026년 5월 기준 학습 과정에서 본인이 체감한 내용으로, 절대적 평가가 아닙니다. 양 생태계 모두 빠르게 변화하고 있어 시점에 따라 비교 결과가 달라질 수 있습니다.*
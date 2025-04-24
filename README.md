# User Authentication & RAG API

이 프로젝트는 대규모 언어 모델(LLM) API를 활용한 사용자 인증 및 RAG(Retrieval-Augmented Generation) 서비스를 제공하는 FastAPI 기반 백엔드입니다.

## 주요 기능

- **사용자 인증 및 관리**
  - 사용자 등록 및 로그인
  - JWT 기반 토큰 인증
  - 보호된 API 엔드포인트 접근 제어
- **RAG(Retrieval-Augmented Generation) 시스템**
  - 문서 업로드 및 관리
  - 자동 문서 청킹(chunking)
  - 임베딩 생성 및 벡터 검색
  - 출처 인용과 함께 응답 생성
- **토큰 사용량 관리**
  - 사용자별 LLM 토큰 사용량 추적
  - 사용자별 임베딩 토큰 사용량 추적
  - 월간 사용량 한도 설정 및 관리

## 실행 방법

```bash
# 저장소 클론
git clone https://github.com/yourusername/user-auth.git
cd user-auth

# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

## 실행행 방법

```bash
# 개발 서버 실행
uvicorn app.main:app --reload

# 프로덕션 서버 실행
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

서버가 실행되면 http://localhost:8000/docs에서 Swagger UI를 통해 API 문서를 확인할 수 있습니다.

## API 엔드포인트

- **인증 관련**
  - POST /register - 새 사용자 등록
  - POST /token - 로그인 및 액세스 토큰 발급
  - GET /users/me - 현재 인증된 사용자 정보 조회
- **RAG 관련**
  - POST /documents - 새 문서 업로드
  - GET /documents - 사용자의 문서 목록 조회
  - POST /conversations - 새 대화 시작
  - POST /conversations/{conversation_id}/messages - 메시지 전송 및 응답 받기

## 프로젝트 구조

- user-auth/
- ├── app/
- │   ├── api/            # API 라우터
- │   ├── auth/           # 인증 관련 코드
- │   ├── core/           # 핵심 설정
- │   │   ├── db.py       # 데이터베이스 연결 설정
- │   │   └── init.py     # 데이터베이스 초기화
- │   ├── crud/           # 데이터베이스 CRUD 작업
- │   ├── models/         # 데이터베이스 모델
- │   └── main.py         # 앱 진입점
- ├── requirements.txt    # 의존성 목록
- └── README.md           # 이 문서

## 환경 설정

프로젝트는 기본적으로 SQLite 데이터베이스를 사용합니다. 데이터베이스 연결 설정은 db.py 파일에서 관리됩니다.

토큰 사용량 관리는 각 사용자별로 설정되며, 기본값은 다음과 같습니다:

 - LLM 토큰 월 한도: 100,000 토큰
 - 임베딩 토큰 월 한도: 100,000 토큰

## 개발 정보

 - 프레임워크: FastAPI
 - 데이터베이스: SQLite + SQLAlchemy ORM
 - 인증: JWT (JSON Web Tokens)
 - 벡터 저장: SQLite JSON 필드 (프로덕션에서는 전용 벡터 데이터베이스 사용 권장)

## 라이선스

MIT License
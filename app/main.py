# app/main.py
from fastapi import FastAPI
from app.core.init import init_db  # db.py 대신 init.py에서 초기화 함수 임포트
from app.api import auth, users

app = FastAPI(
    title="사용자 인증 API",
    description="JWT 토큰 기반 사용자 인증 API",
    version="1.0.0",
    swagger_ui_init_oauth={},  # OAuth2 스키마 제거
)

# 앱 시작 시 데이터베이스 초기화
@app.on_event("startup")
def startup_event():
    init_db()  # 모델 등록 및 테이블 생성

# 라우터 등록
app.include_router(auth.router)
app.include_router(users.router)

# 루트 경로
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "사용자 인증 API에 오신 것을 환영합니다!"}
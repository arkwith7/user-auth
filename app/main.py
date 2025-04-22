# app/main.py
from fastapi import FastAPI
from app.db import engine, Base
from app.api import router as api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router)

# 필요하다면 다른 라우터들도 추가할 수 있습니다.
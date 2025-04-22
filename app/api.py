# app/api.py
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import crud, models
from app.db import get_db
from app.auth import security, jwt

# Pydantic 모델 정의
class UserCreate(BaseModel):
    email: str
    password: str

# 기존 라우터 객체
router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 딕셔너리로 변환하여 전달
    user_data = user.dict()
    return crud.user.create_user(db=db, user=user_data)


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = crud.user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = security.timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def read_users_me(current_user: models.User = Depends(jwt.get_current_user)):
    return {"email": current_user.email, "id": current_user.id}

@router.get("/protected")
async def protected_route(current_user: models.User = Depends(jwt.get_current_user)):
    return {"message": f"Hello, {current_user.email}! This is a protected route."}
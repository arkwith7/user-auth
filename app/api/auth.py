# app/api/auth.py
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import crud, models
from app.auth import security, jwt
from app.core.db import get_db

# 로그인 요청을 위한 모델
class LoginRequest(BaseModel):
    username: str
    password: str

# 사용자 생성 모델
class UserCreate(BaseModel):
    email: str
    password: str

# 보안 스키마 정의
security_scheme = jwt.security_scheme

# 인증 관련 라우터 (auth)
router = APIRouter(
    prefix="/auth",
    tags=["인증"],
    responses={401: {"description": "인증되지 않음"}},
)

@router.post("/register", summary="일반 사용자 등록")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = user.dict()
    return crud.user.create_user(db=db, user=user_data)

@router.post("/token", summary="JWT 토큰 발급")
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = crud.user.get_user_by_email(db, email=login_data.username)
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = security.timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", summary="내 정보 조회")
async def read_users_me(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    current_user: models.User = Depends(jwt.get_current_user)
):
    return {
        "email": current_user.email, 
        "id": current_user.id,
        "is_active": current_user.is_active,
        "is_admin": current_user.is_admin,
        "timestamp": security.datetime.now().isoformat()
    }

@router.get("/protected", summary="보호된 리소스 접근")
async def protected_route(
    credentials: HTTPAuthorizationCredentials = Security(security_scheme),
    current_user: models.User = Depends(jwt.get_current_user)
):
    return {
        "message": f"Hello, {current_user.email}! This is a protected route.",
        "status": "authenticated",
        "timestamp": security.datetime.now().isoformat()
    }
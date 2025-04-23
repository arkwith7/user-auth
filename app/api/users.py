# app/api/users.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app import crud, models
from app.auth import jwt, security
from app.core.db import get_db

# 사용자 응답 모델
class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool
    
    model_config = {
        "from_attributes": True
    }

# 사용자 업데이트 모델
class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None

# 관리자용 사용자 생성 모델
class AdminUserCreate(BaseModel):
    email: str
    password: str
    is_active: bool = True
    is_admin: bool = False

# 보안 스키마
security_scheme = jwt.security_scheme

# 사용자 관리 라우터
router = APIRouter(
    prefix="/users",
    tags=["사용자 관리"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[UserResponse], summary="모든 사용자 목록 조회")
async def get_users(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(jwt.get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security_scheme)
):
    # 관리자 권한 체크는 나중에 구현
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/{user_id}", response_model=UserResponse, summary="특정 사용자 정보 조회")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(jwt.get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security_scheme)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return user

@router.put("/{user_id}", response_model=UserResponse, summary="사용자 정보 수정")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(jwt.get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security_scheme)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data and update_data["password"]:
        update_data["hashed_password"] = security.get_password_hash(update_data.pop("password"))
    
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", summary="사용자 삭제")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(jwt.get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security_scheme)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    
    db.delete(user)
    db.commit()
    return {"detail": "사용자가 성공적으로 삭제되었습니다"}

@router.post("/", response_model=UserResponse, summary="새로운 사용자 등록(관리자용)")
async def create_user(
    user: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(jwt.get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(security_scheme)
):
    # 나중에 관리자 권한 체크 추가 가능
    db_user = crud.user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = user.dict()
    return crud.user.create_user(db=db, user=user_data)
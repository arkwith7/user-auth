# app/crud/user.py
from typing import Dict, List, Optional, Union
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: dict):
    print("Creating user:", user)
    hashed_password = get_password_hash(user['password'])
    db_user = User(
        email=user['email'],
        hashed_password=hashed_password,
        is_active=True,
        is_admin=user.get('is_admin', False)  # 기본값은 False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: Dict[str, any]):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
        
    # 비밀번호 변경 시 해싱 처리
    if "password" in user_data and user_data["password"]:
        user_data["hashed_password"] = get_password_hash(user_data.pop("password"))
    
    # 업데이트할 항목 적용
    for key, value in user_data.items():
        if hasattr(db_user, key) and value is not None:
            setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return False
        
    db.delete(db_user)
    db.commit()
    return True

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# 추가적인 유틸리티 함수 (필요에 따라)
def is_admin(user: User) -> bool:
    """사용자가 관리자인지 확인합니다. 필요에 따라 구현하세요."""
    # User 모델에 is_admin 필드가 있다면:
    # return user.is_admin
    
    # 예시 구현 (고정된 관리자 이메일)
    admin_emails = ["admin@example.com"]
    return user.email in admin_emails
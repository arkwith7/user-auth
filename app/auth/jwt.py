# app/auth/jwt.py
from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import models
from app.core.db import get_db
from app.auth import security

# HTTPBearer 보안 스키마 정의
security_scheme = HTTPBearer(description="JWT 인증 토큰이 필요합니다")

# 토큰에서 현재 사용자 정보 추출
async def get_current_user(
    credentials: str = Security(security_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 토큰은 credentials.credentials에서 가져옵니다
        token = credentials.credentials
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
# app/crud/user.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.auth.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: dict):
    print("Creating user:", user)
    hashed_password = get_password_hash(user['password'])
    db_user = User(
        email=user['email'],
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
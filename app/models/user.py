# app/models/user.py
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.orm import relationship
import datetime

from app.core.db import Base

# 5. User 모델 업데이트 - 관계 추가
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)  # 관리자 권한 필드 추가
    
    # 사용자 생성 및 갱신 시간
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 토큰 사용량 제한 설정
    monthly_llm_token_limit = Column(Integer, default=100000)  # LLM 토큰 월 한도
    monthly_embedding_token_limit = Column(Integer, default=100000)  # 임베딩 토큰 월 한도
    
    # 현재 사용량 트래킹
    llm_tokens_used_this_month = Column(Integer, default=0)
    embedding_tokens_used_this_month = Column(Integer, default=0)
    last_token_reset_date = Column(DateTime, default=datetime.datetime.utcnow)
    
    # RAG 관련 사용자 설정
    default_rag_settings = Column(JSON, default=lambda: {
        "chunk_size": 1000,
        "chunk_overlap": 200,
        "top_k": 3,
        "default_llm_model": "gpt-3.5-turbo",
        "default_embedding_model": "text-embedding-ada-002"
    })
    
    # 관계 - 문자열로 참조하여 순환 참조 해결
    token_usages = relationship("TokenUsage", back_populates="user", foreign_keys="TokenUsage.user_id")
    embedding_usages = relationship("EmbeddingUsage", back_populates="user", foreign_keys="EmbeddingUsage.user_id")
    documents = relationship("Document", back_populates="user", foreign_keys="Document.user_id")
    conversations = relationship("Conversation", back_populates="user", foreign_keys="Conversation.user_id")
# app/models/token_usage.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
import datetime

from app.core.db import Base

# 2. LLM 토큰 사용량 추적 테이블

class TokenUsage(Base):
    __tablename__ = "token_usages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 요청 정보
    request_id = Column(String, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="SET NULL"), nullable=True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    
    # 모델 정보
    model = Column(String)  # 사용한 LLM 모델
    
    # 토큰 사용량
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    # 비용 추적 (USD)
    cost = Column(Float, default=0.0)  
    
    # 추가 메타데이터
    request_metadata = Column(JSON, nullable=True)  # 요청 매개변수 등
    
    # 시간 정보
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 관계
    user = relationship("User", back_populates="token_usages")
    conversation = relationship("Conversation", back_populates="token_usages")
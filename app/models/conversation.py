# app/models/conversation.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Enum
from sqlalchemy.orm import relationship
import datetime
import enum

from app.core.db import Base

# 3. Conversation 및 Message 모델 - 대화 히스토리 관리
class MessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 대화 메타데이터
    title = Column(String, nullable=True)  # 대화 제목 (첫 메시지 기반으로 자동 생성 가능)
    context = Column(String, nullable=True)  # 대화 컨텍스트 설명
    
    # 시간 정보
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 관계
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    token_usages = relationship("TokenUsage", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    
    # 메시지 내용
    role = Column(Enum(MessageRole))
    content = Column(Text)
    
    # 메시지 순서
    sequence = Column(Integer)
    
    # RAG 관련 정보
    query_embedding = Column(JSON, nullable=True)  # 질문 임베딩 (검색에 사용된)
    tokens_used = Column(Integer, nullable=True)  # 토큰 사용량
    model_used = Column(String, nullable=True)  # 사용된 모델
    
    # 메타 정보
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 관계
    conversation = relationship("Conversation", back_populates="messages")
    citations = relationship("Citation", back_populates="message")
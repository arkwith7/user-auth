# app/models/embedding_usage.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship
import datetime
import enum

from app.core.db import Base

# 3. 임베딩 토큰 사용량 추적 테이블

class EmbeddingPurpose(str, enum.Enum):
    DOCUMENT_INDEXING = "document_indexing"
    QUERY = "query"

class EmbeddingUsage(Base):
    __tablename__ = "embedding_usages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 임베딩 정보
    model = Column(String)  # 사용한 임베딩 모델
    purpose = Column(Enum(EmbeddingPurpose))  # 임베딩 용도
    
    # 관련 객체 정보
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="SET NULL"), nullable=True)
    chunk_id = Column(Integer, ForeignKey("chunks.id", ondelete="SET NULL"), nullable=True)
    message_id = Column(Integer, ForeignKey("messages.id", ondelete="SET NULL"), nullable=True)
    
    # 토큰 사용량
    token_count = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    
    # 시간 정보
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 관계
    user = relationship("User", back_populates="embedding_usages")
    document = relationship("Document", back_populates="embedding_usages")
    chunk = relationship("Chunk", back_populates="embedding_usage")
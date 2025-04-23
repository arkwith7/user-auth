# app/models/chunk.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY  # PostgreSQL을 사용하는 경우
import datetime

from app.core.db import Base

# 2. Chunk 모델 - 청킹된 문서 조각 및 임베딩 관리
class Chunk(Base):
    __tablename__ = "chunks"
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"))
    
    # 청크 콘텐츠
    content = Column(Text)  # 청크 텍스트 내용
    
    # 메타데이터
    chunk_index = Column(Integer)  # 문서 내 순서
    page_number = Column(Integer, nullable=True)  # PDF 페이지 번호
    section = Column(String, nullable=True)  # 섹션/챕터 정보
    
    # 벡터 임베딩 - 두 가지 방법 중 선택
    # 1. PostgreSQL의 경우 (vector 확장 사용시)
    # embedding = Column(ARRAY(Float))  # 벡터 임베딩
    # 2. 일반적인 DB의 경우 - JSON으로 저장
    embedding = Column(JSON, nullable=True)  # 벡터 임베딩
    embedding_model = Column(String, nullable=True)  # 임베딩 생성에 사용된 모델
    
    # 메타 정보
    token_count = Column(Integer, nullable=True)  # 토큰 수
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 관계
    document = relationship("Document", back_populates="chunks")
    citations = relationship("Citation", back_populates="chunk")
    embedding_usage = relationship("EmbeddingUsage", back_populates="chunk", uselist=False)
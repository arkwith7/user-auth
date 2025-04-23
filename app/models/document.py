# app/models/document.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
import datetime
import enum
from typing import List

from app.core.db import Base

# 1.Document 모델 - 문서 원본 관리
class DocumentType(str, enum.Enum):
    PDF = "pdf"
    TXT = "txt"
    DOCX = "docx"
    HTML = "html"
    MARKDOWN = "md"

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 문서 메타데이터
    title = Column(String)
    description = Column(String, nullable=True)
    file_name = Column(String)
    file_type = Column(String)  # 파일 확장자 또는 MIME 타입
    doc_type = Column(String)   # 문서 유형 (enum으로 관리 가능)
    
    # 문서 위치 정보
    file_path = Column(String)  # 스토리지 내 경로 (S3 등)
    original_url = Column(String, nullable=True)  # 원본 URL (웹에서 가져온 경우)
    
    # 문서 메타 정보
    author = Column(String, nullable=True)
    published_date = Column(DateTime, nullable=True)
    page_count = Column(Integer, nullable=True)
    word_count = Column(Integer, nullable=True)
    
    # 처리 상태
    is_processed = Column(Boolean, default=False)  # 청킹 및 임베딩 완료 여부
    processing_error = Column(String, nullable=True)
    
    # 공개/비공개 설정
    is_public = Column(Boolean, default=False)
    
    # 시간 정보
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # 관계
    user = relationship("User", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    embedding_usages = relationship("EmbeddingUsage", back_populates="document")

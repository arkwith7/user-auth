# app/models/citation.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
import datetime

from app.core.db import Base

# 4. Citation 모델 - 답변의 출처 관리
class Citation(Base):
    __tablename__ = "citations"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("messages.id"))
    chunk_id = Column(Integer, ForeignKey("chunks.id"))
    
    # 인용 메타데이터
    relevance_score = Column(Float)  # 관련성 점수
    quoted_content = Column(Text, nullable=True)  # 실제 인용된 텍스트
    quote_start_idx = Column(Integer, nullable=True)  # 원본 텍스트에서의 시작 위치 (선택적)
    quote_end_idx = Column(Integer, nullable=True)  # 원본 텍스트에서의 끝 위치 (선택적)
    
    # 시간 정보
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # 관계
    message = relationship("Message", back_populates="citations")
    chunk = relationship("Chunk", back_populates="citations")
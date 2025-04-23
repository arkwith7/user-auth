from app.core.db import Base, engine

# 모든 모델 임포트
# 이렇게 임포트하면 Base.metadata에 모델이 등록됩니다
from app.models.user import User
from app.models.token_usage import TokenUsage
from app.models.embedding_usage import EmbeddingUsage
from app.models.document import Document
from app.models.chunk import Chunk
from app.models.conversation import Conversation, Message
from app.models.citation import Citation
# 기타 모델들...

def init_db():
    # 여기서 테이블 생성
    Base.metadata.create_all(bind=engine)
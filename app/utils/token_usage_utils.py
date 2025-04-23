# app/utils/token_usage_utils.py
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.token_usage import TokenUsage
from app.models.embedding_usage import EmbeddingUsage, EmbeddingPurpose

# 4. 토큰 사용량 관리를 위한 유틸리티 함수

def record_llm_usage(
    db: Session, 
    user_id: int, 
    request_id: str,
    model: str, 
    prompt_tokens: int, 
    completion_tokens: int,
    conversation_id: int = None,
    message_id: int = None,
    metadata: dict = None
):
    """LLM API 사용 기록 및 사용자 토큰 사용량 업데이트"""
    # 비용 계산 (모델별 다른 요금 적용)
    total_tokens = prompt_tokens + completion_tokens
    cost = calculate_llm_cost(model, prompt_tokens, completion_tokens)
    
    # 토큰 사용량 기록
    token_usage = TokenUsage(
        user_id=user_id,
        request_id=request_id,
        conversation_id=conversation_id,
        message_id=message_id,
        model=model,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total_tokens,
        cost=cost,
        metadata=metadata
    )
    db.add(token_usage)
    
    # 사용자 월간 토큰 사용량 업데이트
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        # 월 초기화 확인
        if should_reset_monthly_usage(user.last_token_reset_date):
            user.llm_tokens_used_this_month = total_tokens
            user.embedding_tokens_used_this_month = 0
            user.last_token_reset_date = datetime.utcnow()
        else:
            user.llm_tokens_used_this_month += total_tokens
    
    db.commit()
    return token_usage

def record_embedding_usage(
    db: Session,
    user_id: int,
    model: str,
    token_count: int,
    purpose: EmbeddingPurpose,
    document_id: int = None,
    chunk_id: int = None,
    message_id: int = None
):
    """임베딩 API 사용 기록 및 사용자 토큰 사용량 업데이트"""
    # 비용 계산
    cost = calculate_embedding_cost(model, token_count)
    
    # 임베딩 사용량 기록
    embedding_usage = EmbeddingUsage(
        user_id=user_id,
        model=model,
        purpose=purpose,
        document_id=document_id,
        chunk_id=chunk_id,
        message_id=message_id,
        token_count=token_count,
        cost=cost
    )
    db.add(embedding_usage)
    
    # 사용자 월간 토큰 사용량 업데이트
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        # 월 초기화 확인
        if should_reset_monthly_usage(user.last_token_reset_date):
            user.llm_tokens_used_this_month = 0
            user.embedding_tokens_used_this_month = token_count
            user.last_token_reset_date = datetime.utcnow()
        else:
            user.embedding_tokens_used_this_month += token_count
    
    db.commit()
    return embedding_usage

def check_token_limit(db: Session, user_id: int, token_type: str, requested_tokens: int):
    """사용자의 토큰 한도 확인"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    
    # 월 초기화 체크
    if should_reset_monthly_usage(user.last_token_reset_date):
        user.llm_tokens_used_this_month = 0
        user.embedding_tokens_used_this_month = 0
        user.last_token_reset_date = datetime.utcnow()
        db.commit()
    
    # 토큰 타입에 따른 한도 확인
    if token_type == "llm":
        return user.llm_tokens_used_this_month + requested_tokens <= user.monthly_llm_token_limit
    elif token_type == "embedding":
        return user.embedding_tokens_used_this_month + requested_tokens <= user.monthly_embedding_token_limit
    
    return False

def should_reset_monthly_usage(last_reset_date):
    """월간 사용량 초기화가 필요한지 확인"""
    now = datetime.utcnow()
    # 다른 월이면 초기화
    return (now.year > last_reset_date.year) or (now.year == last_reset_date.year and now.month > last_reset_date.month)

def calculate_llm_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """LLM 모델 사용 비용 계산"""
    rates = {
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002},
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-4-turbo": {"prompt": 0.01, "completion": 0.03},
        # 다른 모델 요금 추가
    }
    
    model_rates = rates.get(model, {"prompt": 0.001, "completion": 0.002})  # 기본값
    cost = (prompt_tokens / 1000 * model_rates["prompt"]) + (completion_tokens / 1000 * model_rates["completion"])
    return cost

def calculate_embedding_cost(model: str, token_count: int) -> float:
    """임베딩 모델 사용 비용 계산"""
    rates = {
        "text-embedding-ada-002": 0.0001,
        # 다른 임베딩 모델 요금 추가
    }
    
    rate = rates.get(model, 0.0001)  # 기본값
    return token_count / 1000 * rate
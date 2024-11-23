from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.divination import DivinationRecord
from app.models.user import User
from app.schemas.divination import DivinationCreate
from app.services.quota import increment_quota
import random
from app.core.cache import cache
from app.services.ai import generate_divination_answer

async def create_divination(
    db: AsyncSession,
    user: User,
    divination_in: DivinationCreate
) -> Optional[DivinationRecord]:
    # 检查并增加用户配额
    if not await increment_quota(db, user):
        return None
    
    # 根据类型生成答案
    answer = await generate_answer(divination_in.type, divination_in.question)
    
    # 创建占卜记录
    divination = DivinationRecord(
        user_id=user.id,
        type=divination_in.type,
        question=divination_in.question,
        answer=answer
    )
    db.add(divination)
    await db.commit()
    await db.refresh(divination)
    return divination

@cache("divination", 3600)
async def get_user_divinations(
    db: AsyncSession,
    user_id: str,
    skip: int = 0,
    limit: int = 10
) -> List[DivinationRecord]:
    result = await db.execute(
        select(DivinationRecord)
        .where(DivinationRecord.user_id == user_id)
        .order_by(DivinationRecord.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@cache("divination", 3600)
async def get_divination(
    db: AsyncSession,
    divination_id: str
) -> Optional[DivinationRecord]:
    result = await db.execute(
        select(DivinationRecord).where(DivinationRecord.id == divination_id)
    )
    return result.scalar_one_or_none()

async def generate_answer(divination_type: str, question: str) -> str:
    """
    生成占卜答案
    """
    # 使用AI生成答案
    answer = await generate_divination_answer(divination_type, question)
    return answer 
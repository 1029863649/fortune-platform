from typing import Optional, List
from datetime import date, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.quota import UserQuota
from app.models.user import User
from app.schemas.quota import QuotaCreate

async def get_user_quota(
    db: AsyncSession,
    user_id: str,
    quota_type: str,
    quota_date: date
) -> Optional[UserQuota]:
    result = await db.execute(
        select(UserQuota).where(
            and_(
                UserQuota.user_id == user_id,
                UserQuota.type == quota_type,
                UserQuota.quota_date == quota_date
            )
        )
    )
    return result.scalar_one_or_none()

async def create_quota(
    db: AsyncSession,
    quota_in: QuotaCreate
) -> UserQuota:
    quota = UserQuota(
        user_id=quota_in.user_id,
        type=quota_in.type,
        quota_date=quota_in.quota_date,
        quota_count=quota_in.quota_count
    )
    db.add(quota)
    await db.commit()
    await db.refresh(quota)
    return quota

async def increment_quota(
    db: AsyncSession,
    user: User,
    quota_type: str = "daily"
) -> bool:
    today = date.today()
    quota = await get_user_quota(db, str(user.id), quota_type, today)
    
    # 如果今天没有配额记录，创建新记录
    if not quota:
        quota_in = QuotaCreate(
            user_id=user.id,
            type=quota_type,
            quota_date=today,
            quota_count=1
        )
        await create_quota(db, quota_in)
        return True
    
    # 检查是否超过配额限制
    quota_limit = get_quota_limit(user.vip_level, quota_type)
    if quota.quota_count >= quota_limit:
        return False
    
    # 增加配额计数
    quota.quota_count += 1
    await db.commit()
    await db.refresh(quota)
    return True

def get_quota_limit(vip_level: int, quota_type: str) -> int:
    """
    根据会员等级和配额类型获取配额限制
    """
    daily_limits = {
        0: 3,    # 普通用户
        1: 10,   # VIP1
        2: 30,   # VIP2
        3: 100,  # VIP3
    }
    return daily_limits.get(vip_level, 3)  # 默认使用普通用户配额

async def check_quota_available(
    db: AsyncSession,
    user: User,
    quota_type: str = "daily"
) -> bool:
    today = date.today()
    quota = await get_user_quota(db, str(user.id), quota_type, today)
    
    if not quota:
        return True
    
    quota_limit = get_quota_limit(user.vip_level, quota_type)
    return quota.quota_count < quota_limit 
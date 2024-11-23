from typing import Dict, Any, List
from datetime import datetime, timedelta
from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.divination import DivinationRecord
from app.models.user import User
from app.models.favorite import Favorite
from app.core.cache import cache

@cache("stats", 3600)
async def get_user_stats(
    db: AsyncSession,
    user_id: str
) -> Dict[str, Any]:
    """获取用户统计数据"""
    # 获取用户总占卜次数
    total_divinations = await db.execute(
        select(func.count(DivinationRecord.id))
        .where(DivinationRecord.user_id == user_id)
    )
    total_count = total_divinations.scalar_one()

    # 获取各类型占卜次数
    type_counts = await db.execute(
        select(DivinationRecord.type, func.count(DivinationRecord.id))
        .where(DivinationRecord.user_id == user_id)
        .group_by(DivinationRecord.type)
    )
    type_stats = dict(type_counts.all())

    # 获取收藏数量
    favorites_count = await db.execute(
        select(func.count(Favorite.id))
        .where(Favorite.user_id == user_id)
    )
    favorites = favorites_count.scalar_one()

    return {
        "total_divinations": total_count,
        "type_stats": type_stats,
        "favorites_count": favorites
    }

@cache("stats", 1800)
async def get_system_stats(db: AsyncSession) -> Dict[str, Any]:
    """获取系统统计数据"""
    now = datetime.utcnow()
    today = now.date()
    
    # 总用户数
    total_users = await db.execute(select(func.count(User.id)))
    
    # 今日新增用户
    new_users = await db.execute(
        select(func.count(User.id))
        .where(func.date(User.created_at) == today)
    )
    
    # 总占卜次数
    total_divinations = await db.execute(
        select(func.count(DivinationRecord.id))
    )
    
    # 今日占卜次数
    today_divinations = await db.execute(
        select(func.count(DivinationRecord.id))
        .where(func.date(DivinationRecord.created_at) == today)
    )
    
    # VIP用户数量
    vip_users = await db.execute(
        select(func.count(User.id))
        .where(User.vip_level > 0)
    )
    
    return {
        "users": {
            "total": total_users.scalar_one(),
            "new_today": new_users.scalar_one(),
            "vip": vip_users.scalar_one()
        },
        "divinations": {
            "total": total_divinations.scalar_one(),
            "today": today_divinations.scalar_one()
        }
    }

@cache("stats", 3600)
async def get_divination_trends(
    db: AsyncSession,
    days: int = 7
) -> List[Dict[str, Any]]:
    """获取占卜趋势数据"""
    now = datetime.utcnow()
    start_date = now - timedelta(days=days)
    
    # 按日期统计占卜次数
    daily_counts = await db.execute(
        select(
            func.date(DivinationRecord.created_at).label('date'),
            func.count(DivinationRecord.id).label('count')
        )
        .where(DivinationRecord.created_at >= start_date)
        .group_by(func.date(DivinationRecord.created_at))
        .order_by('date')
    )
    
    return [
        {
            "date": str(date),
            "count": count
        }
        for date, count in daily_counts.all()
    ] 
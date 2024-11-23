from datetime import date, timedelta
from typing import Optional, List
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.checkin import CheckIn
from app.schemas.checkin import CheckInResponse, CheckInStatus, CheckInHistory, CheckInStats
from app.core.cache import cache, clear_cache
from app.services.quota import add_quota

async def create_checkin(
    db: AsyncSession,
    user_id: str
) -> CheckInResponse:
    """创建签到记录"""
    # 获取连续签到天数
    streak = await get_user_streak(db, user_id)
    
    # 计算奖励配额
    reward = calculate_reward(streak)
    
    # 创建签到记录
    checkin = CheckIn(
        user_id=user_id,
        check_date=date.today(),
        reward=reward
    )
    
    db.add(checkin)
    await db.commit()
    await db.refresh(checkin)
    
    # 添加奖励配额
    await add_quota(db, user_id, reward)
    
    # 清除缓存
    clear_cache_func = clear_cache(
        "checkin",
        f"get_user_streak:{user_id}",
        f"get_user_checkin_status:{user_id}",
        f"get_user_checkin_stats:{user_id}"
    )
    await clear_cache_func()
    
    return CheckInResponse(
        success=True,
        message="签到成功",
        streak=streak + 1,
        reward=reward
    )

@cache("checkin", 3600)
async def get_user_streak(
    db: AsyncSession,
    user_id: str
) -> int:
    """获取用户当前连续签到天数"""
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # 检查昨天是否签到
    result = await db.execute(
        select(CheckIn)
        .where(
            and_(
                CheckIn.user_id == user_id,
                CheckIn.check_date == yesterday
            )
        )
    )
    if not result.scalar_one_or_none():
        return 0
    
    # 计算连续签到天数
    streak = 1
    current_date = yesterday - timedelta(days=1)
    
    while True:
        result = await db.execute(
            select(CheckIn)
            .where(
                and_(
                    CheckIn.user_id == user_id,
                    CheckIn.check_date == current_date
                )
            )
        )
        if not result.scalar_one_or_none():
            break
        
        streak += 1
        current_date -= timedelta(days=1)
    
    return streak

@cache("checkin", 3600)
async def get_user_checkin_status(
    db: AsyncSession,
    user_id: str
) -> CheckInStatus:
    """获取用户今日签到状态"""
    today = date.today()
    
    # 检查今日是否已签到
    result = await db.execute(
        select(CheckIn)
        .where(
            and_(
                CheckIn.user_id == user_id,
                CheckIn.check_date == today
            )
        )
    )
    checked = result.scalar_one_or_none() is not None
    
    # 获取连续签到天数
    streak = await get_user_streak(db, user_id)
    if checked:
        streak += 1
    
    return CheckInStatus(
        checked=checked,
        streak=streak,
        next_reward=calculate_next_reward(streak)
    )

@cache("checkin", 3600)
async def get_user_checkin_stats(
    db: AsyncSession,
    user_id: str
) -> CheckInStats:
    """获取用户签到统计信息"""
    # 获取总签到天数
    total_days_result = await db.execute(
        select(func.count(CheckIn.id))
        .where(CheckIn.user_id == user_id)
    )
    total_days = total_days_result.scalar_one()
    
    # 获取总奖励
    total_rewards_result = await db.execute(
        select(func.sum(CheckIn.reward))
        .where(CheckIn.user_id == user_id)
    )
    total_rewards = total_rewards_result.scalar_one() or 0
    
    # 获取最大连续签到天数
    max_streak = await get_max_streak(db, user_id)
    
    # 获取当前连续签到天数
    current_streak = await get_user_streak(db, user_id)
    
    # 获取最近30天的签到历史
    end_date = date.today()
    start_date = end_date - timedelta(days=29)
    history = await get_user_checkin_history(db, user_id, start_date, end_date)
    
    return CheckInStats(
        total_days=total_days,
        total_rewards=total_rewards,
        max_streak=max_streak,
        current_streak=current_streak,
        history=history
    )

async def get_user_checkin_history(
    db: AsyncSession,
    user_id: str,
    start_date: date,
    end_date: date
) -> List[CheckInHistory]:
    """获取用户签到历史记录"""
    result = await db.execute(
        select(CheckIn)
        .where(
            and_(
                CheckIn.user_id == user_id,
                CheckIn.check_date.between(start_date, end_date)
            )
        )
        .order_by(CheckIn.check_date.desc())
    )
    checkins = result.scalars().all()
    
    # 构建日期范围内的所有日期记录
    history = []
    current_date = end_date
    checkin_dict = {c.check_date: c for c in checkins}
    
    while current_date >= start_date:
        checkin = checkin_dict.get(current_date)
        history.append(
            CheckInHistory(
                date=current_date,
                checked=checkin is not None,
                reward=checkin.reward if checkin else None
            )
        )
        current_date -= timedelta(days=1)
    
    return history

def calculate_reward(streak: int) -> int:
    """计算签到奖励配额"""
    base_reward = 5
    if streak >= 29:  # 连续签到30天
        return base_reward * 3
    elif streak >= 14:  # 连续签到15天
        return base_reward * 2
    elif streak >= 6:  # 连续签到7天
        return int(base_reward * 1.5)
    return base_reward

def calculate_next_reward(streak: int) -> int:
    """计算下一次签到的奖励配额"""
    return calculate_reward(streak + 1)

async def get_max_streak(db: AsyncSession, user_id: str) -> int:
    """获取历史最大连续签到天数"""
    result = await db.execute(
        select(CheckIn)
        .where(CheckIn.user_id == user_id)
        .order_by(CheckIn.check_date.desc())
    )
    checkins = result.scalars().all()
    
    if not checkins:
        return 0
        
    max_streak = current_streak = 1
    for i in range(1, len(checkins)):
        if (checkins[i-1].check_date - checkins[i].check_date).days == 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
            
    return max_streak
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.schemas.checkin import CheckInResponse, CheckInStatus, CheckInHistory, CheckInStats
from app.services.checkin import (
    create_checkin,
    get_user_checkin_status,
    get_user_checkin_history,
    get_user_checkin_stats,
    calculate_next_reward,
    get_user_streak
)
from datetime import date, timedelta

router = APIRouter()

@router.post("", response_model=CheckInResponse)
async def checkin(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """用户签到"""
    # 检查今日是否已签到
    status = await get_user_checkin_status(db, str(current_user.id))
    if status.checked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="今日已签到"
        )
    
    # 执行签到
    return await create_checkin(db, str(current_user.id))

@router.get("/status", response_model=CheckInStatus)
async def get_status(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """获取签到状态"""
    return await get_user_checkin_status(db, str(current_user.id))

@router.get("/history", response_model=list[CheckInHistory])
async def get_history(
    days: int = 7,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """获取签到历史"""
    # 限制查询天数
    if days > 30:
        days = 30
    
    end_date = date.today()
    start_date = end_date - timedelta(days=days-1)
    
    return await get_user_checkin_history(
        db, 
        str(current_user.id),
        start_date,
        end_date
    )

@router.get("/stats", response_model=CheckInStats)
async def get_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """获取签到统计"""
    return await get_user_checkin_stats(db, str(current_user.id))

@router.get("/streak", response_model=dict)
async def get_streak(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """获取连续签到天数"""
    streak = await get_user_streak(db, str(current_user.id))
    return {
        "streak": streak,
        "next_reward": calculate_next_reward(streak)
    }
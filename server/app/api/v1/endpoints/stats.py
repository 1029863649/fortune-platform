from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.services.stats import (
    get_user_stats,
    get_system_stats,
    get_divination_trends
)

router = APIRouter()

@router.get("/me")
async def read_user_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    获取当前用户统计数据
    """
    return await get_user_stats(db, str(current_user.id))

@router.get("/system")
async def read_system_stats(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    获取系统统计数据（仅管理员）
    """
    return await get_system_stats(db)

@router.get("/trends")
async def read_divination_trends(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_superuser),
    days: int = 7
) -> Any:
    """
    获取占卜趋势数据（仅管理员）
    """
    return await get_divination_trends(db, days) 
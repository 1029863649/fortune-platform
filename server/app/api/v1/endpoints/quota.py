from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.schemas.quota import Quota
from app.services.quota import get_user_quota, get_quota_limit
from datetime import date

router = APIRouter()

@router.get("/me", response_model=dict)
async def get_my_quota(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    获取当前用户的配额信息
    """
    today = date.today()
    daily_quota = await get_user_quota(db, str(current_user.id), "daily", today)
    quota_limit = get_quota_limit(current_user.vip_level, "daily")
    
    return {
        "daily_used": daily_quota.quota_count if daily_quota else 0,
        "daily_limit": quota_limit,
        "vip_level": current_user.vip_level,
        "vip_expire": current_user.vip_expire
    } 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.schemas.settings import Settings
from app.services.settings import get_user_settings, update_user_settings

router = APIRouter()

@router.get("/me/settings", response_model=Settings)
async def get_settings(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    """获取用户设置"""
    settings = await get_user_settings(db, current_user)
    return settings

@router.put("/me/settings", response_model=Settings)
async def update_settings(
    *,
    db: AsyncSession = Depends(deps.get_db),
    settings_in: Settings,
    current_user: User = Depends(deps.get_current_active_user)
):
    """更新用户设置"""
    settings = await update_user_settings(db, current_user, settings_in)
    return settings 
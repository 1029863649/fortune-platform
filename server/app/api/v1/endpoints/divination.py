from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.schemas.divination import Divination, DivinationCreate
from app.services.divination import (
    create_divination,
    get_user_divinations,
    get_divination
)

router = APIRouter()

@router.post("", response_model=Divination)
async def create_divination_record(
    *,
    db: AsyncSession = Depends(deps.get_db),
    divination_in: DivinationCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    创建占卜记录
    """
    divination = await create_divination(db, current_user, divination_in)
    if not divination:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="今日占卜次数已达上限"
        )
    return divination

@router.get("/me", response_model=List[Divination])
async def read_user_divinations(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 10
) -> Any:
    """
    获取用户的占卜历史记录
    """
    divinations = await get_user_divinations(
        db, str(current_user.id), skip=skip, limit=limit
    )
    return divinations

@router.get("/{divination_id}", response_model=Divination)
async def read_divination(
    *,
    db: AsyncSession = Depends(deps.get_db),
    divination_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    获取特定占卜记录
    """
    divination = await get_divination(db, divination_id)
    if not divination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="占卜记录不存在"
        )
    if divination.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="没有权限访问该记录"
        )
    return divination 
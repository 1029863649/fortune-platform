from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.models.user import User
from app.schemas.favorite import Favorite, FavoriteCreate
from app.services.favorite import (
    create_favorite,
    delete_favorite,
    get_user_favorites,
    check_is_favorite
)

router = APIRouter()

@router.post("", response_model=Favorite)
async def add_favorite(
    *,
    db: AsyncSession = Depends(deps.get_db),
    favorite_in: FavoriteCreate,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    添加收藏
    """
    # 检查是否已经收藏
    if await check_is_favorite(db, str(current_user.id), str(favorite_in.record_id)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经收藏过该记录"
        )
    
    favorite = await create_favorite(db, current_user, favorite_in)
    return favorite

@router.delete("/{record_id}", response_model=dict)
async def remove_favorite(
    *,
    db: AsyncSession = Depends(deps.get_db),
    record_id: str,
    current_user: User = Depends(deps.get_current_active_user)
) -> Any:
    """
    取消收藏
    """
    if not await delete_favorite(db, current_user, record_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="收藏记录不存在"
        )
    return {"message": "取消收藏成功"}

@router.get("/me", response_model=List[Favorite])
async def read_user_favorites(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 10
) -> Any:
    """
    获取用户的收藏列表
    """
    favorites = await get_user_favorites(
        db, str(current_user.id), skip=skip, limit=limit
    )
    return favorites 
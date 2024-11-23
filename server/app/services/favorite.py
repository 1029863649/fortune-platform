from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.favorite import Favorite
from app.models.user import User
from app.schemas.favorite import FavoriteCreate

async def create_favorite(
    db: AsyncSession,
    user: User,
    favorite_in: FavoriteCreate
) -> Favorite:
    favorite = Favorite(
        user_id=user.id,
        record_id=favorite_in.record_id
    )
    db.add(favorite)
    await db.commit()
    await db.refresh(favorite)
    return favorite

async def delete_favorite(
    db: AsyncSession,
    user: User,
    record_id: str
) -> bool:
    result = await db.execute(
        select(Favorite).where(
            and_(
                Favorite.user_id == user.id,
                Favorite.record_id == record_id
            )
        )
    )
    favorite = result.scalar_one_or_none()
    if not favorite:
        return False
    
    await db.delete(favorite)
    await db.commit()
    return True

async def get_user_favorites(
    db: AsyncSession,
    user_id: str,
    skip: int = 0,
    limit: int = 10
) -> List[Favorite]:
    result = await db.execute(
        select(Favorite)
        .where(Favorite.user_id == user_id)
        .order_by(Favorite.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def check_is_favorite(
    db: AsyncSession,
    user_id: str,
    record_id: str
) -> bool:
    result = await db.execute(
        select(Favorite).where(
            and_(
                Favorite.user_id == user_id,
                Favorite.record_id == record_id
            )
        )
    )
    return result.scalar_one_or_none() is not None 
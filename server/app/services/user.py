from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password
from app.core.cache import cache, clear_cache

@cache("user", 3600)
async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

@cache("user", 3600)
async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        is_active=True,
        is_superuser=False,
        vip_level=0
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def update_user(
    db: AsyncSession, 
    current_user: User,
    user_in: UserUpdate
) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    
    # 如果要更新密码
    if "password" in update_data:
        hashed_password = get_password_hash(update_data["password"])
        del update_data["password"]
        update_data["hashed_password"] = hashed_password
    
    # 更新用户数据
    for field, value in update_data.items():
        setattr(current_user, field, value)
    
    await db.commit()
    await db.refresh(current_user)
    
    # 清除用户缓存
    clear_cache_func = clear_cache("user", f"get_user_by_email:{current_user.email}", 
                                 f"get_user_by_username:{current_user.username}")
    await clear_cache_func()
    
    return current_user

async def change_password(
    db: AsyncSession,
    current_user: User,
    current_password: str,
    new_password: str
) -> bool:
    if not verify_password(current_password, current_user.hashed_password):
        return False
    
    current_user.hashed_password = get_password_hash(new_password)
    await db.commit()
    return True 
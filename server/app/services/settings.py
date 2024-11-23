from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.settings import Settings
from app.core.cache import cache, clear_cache

@cache("settings", 3600)
async def get_user_settings(db: AsyncSession, user: User) -> Settings:
    """获取用户设置"""
    if not user.settings:
        # 返回默认设置
        return Settings()
    return Settings(**user.settings)

async def update_user_settings(
    db: AsyncSession,
    user: User,
    settings: Settings
) -> Settings:
    """更新用户设置"""
    user.settings = settings.model_dump()
    await db.commit()
    
    # 清除缓存
    clear_cache_func = clear_cache("settings", f"get_user_settings:{user.id}")
    await clear_cache_func()
    
    return settings 
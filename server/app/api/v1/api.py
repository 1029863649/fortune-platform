from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth, users, quota, divination, favorites, 
    monitor, stats, checkin, settings
)

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(users.router, prefix="/users", tags=["用户"])
api_router.include_router(quota.router, prefix="/quota", tags=["配额"])
api_router.include_router(divination.router, prefix="/divination", tags=["占卜"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["收藏"])
api_router.include_router(monitor.router, prefix="/monitor", tags=["监控"])
api_router.include_router(stats.router, prefix="/stats", tags=["统计"])
api_router.include_router(checkin.router, prefix="/checkin", tags=["签到"])
api_router.include_router(settings.router, prefix="/settings", tags=["设置"]) 
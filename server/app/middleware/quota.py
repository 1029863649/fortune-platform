from typing import Callable
from fastapi import Request, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.quota import check_quota_available
from app.api import deps

async def quota_check_middleware(
    request: Request,
    call_next: Callable,
) -> bool:
    # 检查是否是需要配额检查的路径
    if not request.url.path.startswith("/api/v1/divination"):
        return await call_next(request)
    
    # 获取当前用户和数据库会话
    user = await deps.get_current_active_user(request)
    db: AsyncSession = request.state.db
    
    # 检查用户配额
    if not await check_quota_available(db, user):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="今日占卜次数已达上限"
        )
    
    return await call_next(request) 
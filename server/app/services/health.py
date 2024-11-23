from typing import Dict, Any
import psutil
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.redis import redis_client

async def check_database(db: AsyncSession) -> bool:
    """检查数据库连接"""
    try:
        await db.execute(text("SELECT 1"))
        return True
    except Exception:
        return False

async def check_redis() -> bool:
    """检查Redis连接"""
    try:
        await redis_client.set("health_check", "ok", expire=1)
        return True
    except Exception:
        return False

async def get_system_health() -> Dict[str, Any]:
    """获取系统健康状态"""
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "cpu": {
            "percent": cpu_percent,
            "status": "healthy" if cpu_percent < 80 else "warning"
        },
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent,
            "status": "healthy" if memory.percent < 80 else "warning"
        },
        "disk": {
            "total": disk.total,
            "free": disk.free,
            "percent": disk.percent,
            "status": "healthy" if disk.percent < 80 else "warning"
        }
    }

async def check_all_services(db: AsyncSession) -> Dict[str, Any]:
    """检查所有服务状态"""
    db_status = await check_database(db)
    redis_status = await check_redis()
    system_health = await get_system_health()
    
    return {
        "status": "healthy" if all([db_status, redis_status]) else "unhealthy",
        "services": {
            "database": "healthy" if db_status else "unhealthy",
            "redis": "healthy" if redis_status else "unhealthy",
        },
        "system": system_health
    } 
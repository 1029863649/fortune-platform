from typing import Any
from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.api import deps
from app.services.health import check_all_services
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

router = APIRouter()

@router.get("/health")
async def health_check(
    db: AsyncSession = Depends(deps.get_db)
) -> Any:
    """
    系统健康检查
    """
    return await check_all_services(db)

@router.get("/metrics")
async def metrics() -> Response:
    """
    Prometheus metrics endpoint
    """
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    ) 
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.exceptions import BaseError
from app.core.error_handlers import (
    validation_error_handler,
    database_error_handler,
    base_error_handler,
    general_error_handler
)
from app.core.logging import setup_logging
from app.middleware.logging import LoggingMiddleware
from app.middleware.metrics import MetricsMiddleware, update_system_metrics
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# 设置日志系统
logger = setup_logging()

app = FastAPI(
    title="天机阁占卜平台",
    description="基于AI的在线占卜平台",
    version="0.1.0",
    contact={
        "name": "仲戌字",
        "url": "https://sanshengshui.com",
        "email": "admin@sanshengshui.com"
    },
    license_info={
        "name": "专有软件",
        "url": "https://sanshengshui.com/license",
    }
)

# 配置中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)

# 注册错误处理器
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(SQLAlchemyError, database_error_handler)
app.add_exception_handler(BaseError, base_error_handler)
app.add_exception_handler(Exception, general_error_handler)

# 注册路由
app.include_router(api_router, prefix=settings.API_V1_STR)

# 创建定时任务调度器
scheduler = AsyncIOScheduler()
# 每60秒更新一次系统指标
scheduler.add_job(update_system_metrics, 'interval', seconds=60)
scheduler.start()

@app.get("/")
async def root():
    logger.info("访问首页")
    return {"message": "欢迎使用天机阁占卜平台API"}

@app.get("/health")
async def health_check():
    logger.info("健康检查")
    return {"status": "healthy"} 
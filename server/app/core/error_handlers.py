from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from .exceptions import BaseError
import logging

logger = logging.getLogger(__name__)

async def validation_error_handler(request: Request, exc: RequestValidationError):
    """处理请求参数验证错误"""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "code": 1005,
            "message": "数据验证失败",
            "errors": exc.errors()
        }
    )

async def database_error_handler(request: Request, exc: SQLAlchemyError):
    """处理数据库错误"""
    logger.error(f"Database error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 1006,
            "message": "数据库操作失败"
        }
    )

async def base_error_handler(request: Request, exc: BaseError):
    """处理自定义基础错误"""
    logger.error(f"Base error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail
    )

async def general_error_handler(request: Request, exc: Exception):
    """处理其他未捕获的错误"""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": 1000,
            "message": "服务器内部错误"
        }
    ) 
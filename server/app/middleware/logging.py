from typing import Callable
import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("access")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        # 记录请求信息
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"Client: {request.client.host if request.client else 'Unknown'}"
        )

        try:
            response = await call_next(request)
            
            # 记录响应信息
            process_time = (time.time() - start_time) * 1000
            logger.info(
                f"Response: {response.status_code} "
                f"Process Time: {process_time:.2f}ms"
            )
            
            return response
            
        except Exception as e:
            # 记录错误信息
            logger.error(
                f"Request failed: {request.method} {request.url.path} "
                f"Error: {str(e)}"
            )
            raise 
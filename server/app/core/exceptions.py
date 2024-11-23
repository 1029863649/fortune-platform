from typing import Any, Optional, Dict
from fastapi import HTTPException, status

class BaseError(HTTPException):
    def __init__(
        self,
        code: int,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        headers: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        super().__init__(status_code=status_code, detail={"code": code, "message": message}, headers=headers)

class AuthError(BaseError):
    """认证相关错误"""
    def __init__(self, message: str = "认证失败", code: int = 1001):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )

class PermissionError(BaseError):
    """权限相关错误"""
    def __init__(self, message: str = "权限不足", code: int = 1002):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_403_FORBIDDEN
        )

class ResourceNotFound(BaseError):
    """资源不存在"""
    def __init__(self, message: str = "资源不存在", code: int = 1003):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_404_NOT_FOUND
        )

class QuotaExceeded(BaseError):
    """配额超限"""
    def __init__(self, message: str = "配额已用完", code: int = 1004):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )

class ValidationError(BaseError):
    """数据验证错误"""
    def __init__(self, message: str = "数据验证失败", code: int = 1005):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class DatabaseError(BaseError):
    """数据库错误"""
    def __init__(self, message: str = "数据库操作失败", code: int = 1006):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 
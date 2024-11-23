from functools import wraps
from typing import Any, Callable
import json
from app.core.redis import redis_client

def cache(prefix: str, expire: int = 3600):
    """
    缓存装饰器
    :param prefix: 缓存键前缀
    :param expire: 过期时间（秒）
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            # 生成缓存键
            cache_key = f"{prefix}:{func.__name__}"
            if args:
                cache_key += f":{':'.join(str(arg) for arg in args)}"
            if kwargs:
                cache_key += f":{':'.join(f'{k}={v}' for k, v in kwargs.items())}"

            # 尝试从缓存获取
            cached_data = await redis_client.get(cache_key)
            if cached_data:
                return json.loads(cached_data)

            # 执行原函数
            result = await func(*args, **kwargs)

            # 存入缓存
            await redis_client.set(
                cache_key,
                json.dumps(result),
                expire=expire
            )

            return result
        return wrapper
    return decorator

def clear_cache(prefix: str, *keys: str):
    """
    清除指定前缀的缓存
    """
    async def _clear():
        for key in keys:
            cache_key = f"{prefix}:{key}"
            await redis_client.delete(cache_key)
    return _clear 
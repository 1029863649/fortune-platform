from typing import Optional, Any
import json
from redis import asyncio as aioredis
from app.core.config import settings

class RedisClient:
    def __init__(self):
        self.redis = None

    async def init(self):
        if not self.redis:
            self.redis = await aioredis.from_url(
                f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
                encoding="utf-8",
                decode_responses=True
            )

    async def get(self, key: str) -> Optional[str]:
        await self.init()
        return await self.redis.get(key)

    async def set(
        self,
        key: str,
        value: Any,
        expire: int = None
    ) -> bool:
        await self.init()
        return await self.redis.set(
            key,
            value if isinstance(value, str) else json.dumps(value),
            ex=expire
        )

    async def delete(self, key: str) -> int:
        await self.init()
        return await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        await self.init()
        return await self.redis.exists(key)

    async def incr(self, key: str) -> int:
        await self.init()
        return await self.redis.incr(key)

    async def close(self):
        if self.redis:
            await self.redis.close()

redis_client = RedisClient() 
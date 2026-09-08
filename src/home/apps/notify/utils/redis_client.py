# -*- coding: utf-8 -*-

import json
from typing import Any, Dict, Optional

import redis.asyncio as aioredis

import home.core as core

_redis_client: Optional[aioredis.Redis] = None


async def get_redis() -> aioredis.Redis:
    global _redis_client
    if _redis_client is None:
        _redis_client = aioredis.Redis(
            host=core.config.REDIS_HOST,
            port=core.config.REDIS_PORT,
            db=core.config.REDIS_DB,
            password=core.config.REDIS_PASSWORD,
            decode_responses=True,
        )
    return _redis_client


class RedisTokenStore:
    """Redis token 存取，用于邮箱验证与密码重置。"""

    def _key(self, purpose: str, token: str) -> str:
        return f"notify:token:{purpose}:{token}"

    async def set_token(self, purpose: str, token: str, payload: Dict[str, Any], ttl: int) -> None:
        client = await get_redis()
        await client.set(self._key(purpose, token), json.dumps(payload), ex=ttl)

    async def get_and_delete_token(self, purpose: str, token: str) -> Optional[Dict[str, Any]]:
        client = await get_redis()
        key = self._key(purpose, token)
        raw = await client.get(key)
        if raw is None:
            return None
        await client.delete(key)
        return json.loads(raw)

# -*- coding: utf-8 -*-

import home.core as core
from home.web import exceptions

from .redis_client import get_redis


async def check_and_record_send(email: str, purpose: str) -> None:
    """同邮箱 5 分钟冷却 + 每小时最多 3 次。"""
    client = await get_redis()
    cooldown_key = f"notify:ratelimit:cooldown:{purpose}:{email}"
    hour_key = f"notify:ratelimit:hour:{purpose}:{email}"

    if await client.exists(cooldown_key):
        raise exceptions.Http429TooManyRequestsException(
            exceptions.Http429TooManyRequestsException.RateLimitExceeded,
            "发送过于频繁，请稍后再试",
        )

    count = await client.incr(hour_key)
    if count == 1:
        await client.expire(hour_key, 3600)
    if count > core.config.EMAIL_RATE_LIMIT_HOURLY_MAX:
        raise exceptions.Http429TooManyRequestsException(
            exceptions.Http429TooManyRequestsException.RateLimitExceeded,
            "发送次数已达上限，请稍后再试",
        )

    await client.set(cooldown_key, "1", ex=core.config.EMAIL_RATE_LIMIT_COOLDOWN)

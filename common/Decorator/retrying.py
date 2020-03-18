#!/usr/bin/python
import functools
import asyncio
import time
from commons.coroutine_utils import is_coroutine


def retry(retry_times=5, fixed_sleep=0, retry_on_exception=Exception, *dargs):
    """
    重试装饰器
    @params retry_times: 重试次数
    @params fixed_sleep: 每次重试固定休息时间
    @params retry_on_exception: 发生指定异常的情况下重试
    """

    def decorator(func):

        if is_coroutine(func):
            @functools.wraps(func)
            async def wrapped(*args, **kwargs):
                for _ in range(retry_times):
                    try:
                        return await func(*args, **kwargs)
                    except retry_on_exception as e:
                        if fixed_sleep > 0:
                            await asyncio.sleep(fixed_sleep)
                return await func(*args, **kwargs)

            return wrapped

        else:
            @functools.wraps(func)
            def wrapped(*args, **kwargs):
                for _ in range(retry_times):
                    try:
                        return func(*args, **kwargs)
                    except retry_on_exception as e:
                        if fixed_sleep > 0:
                            time.sleep(fixed_sleep)
                return func(*args, **kwargs)

            return wrapped

    if len(dargs) and callable(dargs[0]):
        return decorator(dargs[0])
    else:
        return decorator

import os
import uuid
import asyncio
import logging
from functools import wraps
from . import redis_helper as redis

logger = logging.getLogger("helper.Helper_rwlock")


class Locked:
    """
    Python 3.7 之后才可以使用asynccontextmanager
    """

    def __init__(self, key, timeout=1):
        self.key = key
        self.timeout = timeout

    async def __aenter__(self):
        while True:
            if await redis.setnx(self.key, timeout=self.timeout):
                break
            asyncio.sleep(0.1)

    async def __aexit__(self, exc_type, exc_value, tb):
        await redis.delete(self.key)


class ReadLocked:
    """
    简介
    ----------
    读锁， 可重入， 与写锁冲突

    """

    def __init__(self, key, timeout=1000):
        self.__init_rdlock_lua = None
        self.__init_rdunlock_lua = None
        self.__init_unlock_lua = None
        self.locked = False
        self.key = key
        self.timeout = timeout
        self.name = str(uuid.uuid4())

    def __call__(self, func):
        if asyncio.iscoroutinefunction(func):

            @wraps(func)
            async def inner(_key, *args, **kwds):
                async with ReadLocked(_key, self.timeout):
                    return await func(_key, *args, **kwds)

            return inner
        else:

            @wraps(func)
            async def inner(_key, *args, **kwds):
                async with ReadLocked(_key, self.timeout):
                    return func(_key, *args, **kwds)

            return inner

    @property
    def rdlock_lua(self):
        if not self.__init_rdlock_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "rwlock_rdlock.lua"), "rb") as fp:
                self.__init_rdlock_lua = fp.read()
        return self.__init_rdlock_lua

    @property
    def rdunlock_lua(self):
        if not self.__init_rdunlock_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "rwlock_rdunlock.lua"), "rb") as fp:
                self.__init_rdunlock_lua = fp.read()
        return self.__init_rdunlock_lua

    @property
    def unlock_lua(self):
        if not self.__init_unlock_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "rwlock_unlock.lua"), "rb") as fp:
                self.__init_unlock_lua = fp.read()
        return self.__init_unlock_lua

    async def __aenter__(self):
        while True:
            result = await redis.run_script(self.rdlock_lua, [self.key], [self.timeout, self.name])
            if result is None:
                self.locked = True
                logger.debug(f"获得{self.key}读锁")
                break
            else:
                await asyncio.sleep(0.1)

    async def __aexit__(self, exc_type, exc_value, tb):
        if self.locked:
            result = await redis.run_script(self.rdunlock_lua, [self.key], [self.name])
            if result is None:
                logger.debug(f"释放{self.key}读锁")
            elif result == 0:
                logger.warning(f"释放{self.key}读锁， 释放失败")
            elif result == 1:
                logger.debug(f"释放{self.key}读锁， 完全释放")

    async def force_unlock(self):
        return await redis.run_script(self.unlock_lua, [self.key], [])


class WriteLocked:
    """
    简介
    ----------
    写锁， 与读锁冲突

    """

    def __init__(self, key, timeout=1000):
        self.__init_wtlock_lua = None
        self.__init_wtunlock_lua = None
        self.__init_unlock_lua = None
        self.locked = False
        self.key = key
        self.timeout = timeout

    def __call__(self, func):
        @wraps(func)
        async def inner(_key, *args, **kwds):
            async with WriteLocked(_key, self.timeout):
                return await func(_key, *args, **kwds)

        return inner

    @property
    def wtlock_lua(self):
        if not self.__init_wtlock_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "rwlock_wtlock.lua"), "rb") as fp:
                self.__init_wtlock_lua = fp.read()
        return self.__init_wtlock_lua

    @property
    def wtunlock_lua(self):
        if not self.__init_wtunlock_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "rwlock_wtunlock.lua"), "rb") as fp:
                self.__init_wtunlock_lua = fp.read()
        return self.__init_wtunlock_lua

    @property
    def unlock_lua(self):
        if not self.__init_unlock_lua:
            with open(os.path.join(os.path.dirname(__file__), "Lua", "rwlock_unlock.lua"), "rb") as fp:
                self.__init_unlock_lua = fp.read()
        return self.__init_unlock_lua

    async def __aenter__(self):
        while True:
            result = await redis.run_script(self.wtlock_lua, [self.key], [self.timeout])
            if result is None:
                self.locked = True
                logger.debug(f"获得{self.key}写锁")
                break
            else:
                await asyncio.sleep(0.1)

    async def __aexit__(self, exc_type, exc_value, tb):
        if self.locked:
            result = await redis.run_script(self.wtunlock_lua, [self.key], [])
            if result is None:
                logger.debug(f"释放{self.key}写锁")
            elif result == 0:
                logger.warning(f"释放{self.key}写锁， 释放失败")
            elif result == 1:
                logger.debug(f"释放{self.key}写锁， 完全释放")

    async def force_unlock(self):
        return await redis.run_script(self.unlock_lua, [self.key], [])

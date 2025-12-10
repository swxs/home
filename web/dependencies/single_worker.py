from typing import Dict, Generic, Optional, Type, TypeVar

from sqlalchemy.exc import (
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine import baseModel
from mysqlengine.repositories import repository_productor
from mysqlengine.repositories.base import BaseRepository

# 本模块方法
from .convert_exception import _convert_db_exception

T = TypeVar("T", bound=baseModel)


class SingleWorker(Generic[T]):
    """管理单个Repository和事务"""

    def __init__(self, db: AsyncSession, model_type: Type[T]):
        self.db = db
        self.repository: BaseRepository[T] = repository_productor[model_type.__tablename__](model_type, self.db)
        self._committed = False

    async def commit(self):
        """提交所有更改"""
        try:
            await self.db.commit()
            self._committed = True
        except (IntegrityError, OperationalError, DataError, ProgrammingError, DatabaseError) as exc:
            # 捕获提交时的数据库异常并转换
            raise _convert_db_exception(exc) from exc

    async def rollback(self):
        """回滚所有更改"""
        try:
            await self.db.rollback()
        except (OperationalError, DatabaseError) as exc:
            # 回滚时也可能出现数据库错误（如连接断开）
            raise _convert_db_exception(exc) from exc

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            # 如果有异常，尝试回滚
            try:
                await self.rollback()
            except Exception:
                # 回滚失败时，忽略回滚异常，保留原始异常
                pass
        elif not self._committed:
            # 如果没有异常且未提交，则提交
            await self.commit()

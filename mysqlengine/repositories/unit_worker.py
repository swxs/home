from typing import Dict, Generic, Type

from sqlalchemy.ext.asyncio import AsyncSession

# 本模块方法
from .. import baseModel
from . import repository_productor
from .base import BaseRepository


class UnitWorker:
    """管理多个Repository和事务"""

    def __init__(self, db: AsyncSession):
        self.db = db
        self._repositories: Dict[Type, BaseRepository] = {}
        self._committed = False

    def get_repository(self, model_type: type[baseModel]) -> BaseRepository[baseModel]:
        """获取或创建Repository"""
        if model_type not in self._repositories:
            self._repositories[model_type] = repository_productor[model_type.__tablename__](model_type, self.db)
        return self._repositories[model_type]

    async def commit(self):
        """提交所有更改"""
        await self.db.commit()
        self._committed = True

    async def rollback(self):
        """回滚所有更改"""
        await self.db.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        elif not self._committed:
            await self.commit()

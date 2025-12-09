from typing import Dict, Generic, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession

# 本模块方法
from .. import baseModel
from . import repository_productor
from .base import BaseRepository


class SingleWorker:
    """管理单个Repository和事务"""

    def __init__(self, db: AsyncSession, model_type: type[baseModel]):
        self.db = db
        self.repository = repository_productor[model_type.__tablename__](model_type, self.db)
        self._committed = False

    async def commit(self, model: Optional[baseModel] = None):
        """提交所有更改"""
        await self.db.commit()
        if model:
            await self.db.refresh(model)
        self._committed = True

    async def rollback(self):
        """回滚所有更改"""
        await self.db.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.db.rollback()
        elif not self._committed:
            await self.db.commit()

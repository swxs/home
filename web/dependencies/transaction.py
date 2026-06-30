# -*- coding: utf-8 -*-
# @File    : dependencies/transaction.py
# @AUTH    : code_creater

"""轻量事务上下文管理器。

仅负责事务边界（commit / rollback）与数据库异常转换，不涉及 repository 获取。
service 在写操作处显式包裹::

    async with transaction(self.db):
        await self.repo.create_one(schema)

只读操作无需包裹。
"""

from contextlib import asynccontextmanager

from sqlalchemy.exc import (
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.asyncio import AsyncSession

# 本模块方法
from .convert_exception import _convert_db_exception


@asynccontextmanager
async def transaction(db: AsyncSession):
    """提交成功路径、回滚异常路径，并转换数据库异常为标准 HTTP 异常。"""
    try:
        yield db
        await db.commit()
    except (IntegrityError, OperationalError, DataError, ProgrammingError, DatabaseError) as exc:
        await db.rollback()
        raise _convert_db_exception(exc) from exc
    except Exception:
        await db.rollback()
        raise

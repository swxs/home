# -*- coding: utf-8 -*-
"""数据库 session 与事务原语（纯 DB 语义，不含 HTTP 异常转换）。"""

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from home.mysqlengine import SessionLocal


@asynccontextmanager
async def open_session():
    """创建并关闭一次数据库会话。供脚本、后台任务等非 HTTP 场景使用。"""
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def transaction(session: AsyncSession):
    """写路径事务边界：成功 commit，异常 rollback 后原样抛出。"""
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise

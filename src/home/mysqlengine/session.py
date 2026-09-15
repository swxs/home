# -*- coding: utf-8 -*-
"""数据库 session 与事务原语（纯 DB 语义，不含 HTTP 异常转换）。"""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession

from home.mysqlengine import SessionLocal

logger = logging.getLogger(__name__)


@asynccontextmanager
async def open_session() -> AsyncIterator[AsyncSession]:
    """创建并在退出时关闭一次数据库会话，供脚本、后台任务等非 HTTP 场景使用。

    退出语义是 close：未 commit 的改动会回滚，不会自动 commit。
    写路径请配合 ``transaction(session)``，或自包含场景使用 ``SessionLocal.begin()``。
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()


@asynccontextmanager
async def transaction(session: AsyncSession) -> AsyncIterator[AsyncSession]:
    """写路径事务边界：成功 commit，异常 rollback 后原样抛出。

    使用规范（后续改代码请遵守）：

    - **不可嵌套**：同一 ``AsyncSession`` 上只能有一层 ``transaction()``。
      SQLAlchemy Session 没有真正的事务嵌套；内层 ``commit()`` 会提交外层事务，
      外层 ``rollback()`` 无法撤销，原子性会静默丢失。
    - **边界放在入口**：Service 的写方法最外层包一层即可；块内只调 Repository，
      不要在此再调其它会包 ``transaction()`` 的 Service 方法。
    - **需要逻辑嵌套**时用 ``await session.begin_nested()``（SAVEPOINT），
      不要嵌套本函数。
    - **多表同一原子单元**应共用一个 ``transaction()`` + 多个 repo，
      不要拆成多个 commit 还指望一起回滚。
    - **commit 后 ORM**：项目已设 ``expire_on_commit=False``；若仍要在出块后读 ORM
      属性，优先在块内 ``model_validate`` 成 DTO。
    """
    try:
        yield session
        await session.commit()
    except BaseException:
        try:
            await session.rollback()
        except Exception:
            logger.exception("事务回滚失败，该会话将在 close 时丢弃")
        raise

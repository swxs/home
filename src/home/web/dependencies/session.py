# -*- coding: utf-8 -*-
"""HTTP 层 session 依赖与事务薄封装：调用 mysqlengine 原语并转换 DB 异常。"""

from contextlib import asynccontextmanager

from sqlalchemy.exc import (
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from home.mysqlengine.session import open_session as _open_session
from home.mysqlengine.session import transaction as _db_transaction

# 本模块方法
from ..exceptions import (
    BaseHttpException,
    Http400BadRequestException,
    Http500InternalServerErrorException,
)

_DB_EXCEPTIONS = (
    IntegrityError,
    OperationalError,
    DataError,
    ProgrammingError,
    DatabaseError,
)


def _convert_db_exception(exc: Exception) -> Exception:
    """将数据库异常转换为标准 HTTP 异常。"""
    if isinstance(exc, IntegrityError):
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        if "Duplicate entry" in error_msg or "UNIQUE constraint" in error_msg:
            error_msg = "数据已存在，违反唯一性约束"
        elif "foreign key constraint" in error_msg.lower() or "FOREIGN KEY" in error_msg:
            error_msg = "数据关联错误，违反外键约束"
        return Http400BadRequestException(Http400BadRequestException.DatabaseConstraintError, error_msg)
    if isinstance(exc, DataError):
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        return Http400BadRequestException(Http400BadRequestException.DatabaseDataError, f"数据格式错误: {error_msg}")
    if isinstance(exc, OperationalError):
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        if "connection" in error_msg.lower() or "connect" in error_msg.lower():
            return Http500InternalServerErrorException(
                Http500InternalServerErrorException.DatabaseConnectionError,
                "数据库连接失败，请稍后重试",
            )
        return Http500InternalServerErrorException(
            Http500InternalServerErrorException.DatabaseError,
            f"数据库操作失败: {error_msg}",
        )
    if isinstance(exc, ProgrammingError):
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        return Http500InternalServerErrorException(
            Http500InternalServerErrorException.DatabaseProgrammingError,
            f"数据库查询错误: {error_msg}",
        )
    if isinstance(exc, DatabaseError):
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        return Http500InternalServerErrorException(
            Http500InternalServerErrorException.DatabaseError,
            f"数据库错误: {error_msg}",
        )
    return Http500InternalServerErrorException(
        Http500InternalServerErrorException.DatabaseError,
        f"数据库操作异常: {str(exc)}",
    )


async def get_session():
    """FastAPI 依赖：请求级 session 分发，并将 DB 异常转为 HTTP 异常。"""
    async with _open_session() as session:
        try:
            yield session
        except _DB_EXCEPTIONS as exc:
            raise _convert_db_exception(exc) from exc
        except BaseHttpException as exc:
            raise exc
        finally:
            await session.close()


@asynccontextmanager
async def transaction(session: AsyncSession):
    """写路径事务边界（HTTP 场景）：commit / rollback + DB 异常转换。"""
    try:
        async with _db_transaction(session):
            yield session
    except _DB_EXCEPTIONS as exc:
        raise _convert_db_exception(exc) from exc

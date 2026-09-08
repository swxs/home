from sqlalchemy.exc import (
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)

# 本模块方法
from ..exceptions import (
    BaseHttpException,
    Http400BadRequestException,
    Http500InternalServerErrorException,
)


def _convert_db_exception(exc: Exception) -> Exception:
    """
    将数据库异常转换为标准HTTP异常

    Args:
        exc: 数据库异常

    Returns:
        转换后的HTTP异常
    """
    if isinstance(exc, IntegrityError):
        # 完整性约束错误（唯一约束、外键约束等）
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        # 提取更友好的错误信息
        if "Duplicate entry" in error_msg or "UNIQUE constraint" in error_msg:
            error_msg = "数据已存在，违反唯一性约束"
        elif "foreign key constraint" in error_msg.lower() or "FOREIGN KEY" in error_msg:
            error_msg = "数据关联错误，违反外键约束"
        return Http400BadRequestException(Http400BadRequestException.DatabaseConstraintError, error_msg)
    elif isinstance(exc, DataError):
        # 数据错误（数据类型不匹配、数据长度超限等）
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        return Http400BadRequestException(Http400BadRequestException.DatabaseDataError, f"数据格式错误: {error_msg}")
    elif isinstance(exc, OperationalError):
        # 数据库操作错误（连接失败、超时等）
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        if "connection" in error_msg.lower() or "connect" in error_msg.lower():
            return Http500InternalServerErrorException(
                Http500InternalServerErrorException.DatabaseConnectionError, "数据库连接失败，请稍后重试"
            )
        return Http500InternalServerErrorException(
            Http500InternalServerErrorException.DatabaseError, f"数据库操作失败: {error_msg}"
        )
    elif isinstance(exc, ProgrammingError):
        # SQL语法错误等编程错误
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        return Http500InternalServerErrorException(
            Http500InternalServerErrorException.DatabaseProgrammingError, f"数据库查询错误: {error_msg}"
        )
    elif isinstance(exc, DatabaseError):
        # 其他数据库错误
        error_msg = str(exc.orig) if hasattr(exc, "orig") else str(exc)
        return Http500InternalServerErrorException(
            Http500InternalServerErrorException.DatabaseError, f"数据库错误: {error_msg}"
        )
    else:
        # 未知的数据库相关异常，转换为通用500错误
        return Http500InternalServerErrorException(
            Http500InternalServerErrorException.DatabaseError, f"数据库操作异常: {str(exc)}"
        )

from sqlalchemy.exc import (
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)

from home.mysqlengine import SessionLocal

# 本模块方法
from ..exceptions import BaseHttpException
from .convert_exception import _convert_db_exception


async def get_db():
    """
    获取数据库会话依赖

    在会话使用过程中捕获数据库异常并转换为标准HTTP异常
    注意：async with 会自动管理会话的生命周期，无需手动关闭
    """
    async with SessionLocal() as session:
        try:
            yield session
        except (IntegrityError, OperationalError, DataError, ProgrammingError, DatabaseError) as exc:
            # 捕获数据库异常并转换
            raise _convert_db_exception(exc) from exc
        except BaseHttpException as exc:
            raise exc
        # 其他异常直接抛出，由全局异常处理器处理
        finally:
            await session.close()

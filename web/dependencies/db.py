from csv import excel

from fastapi.param_functions import Depends
from sqlalchemy.exc import (
    DataError,
    DatabaseError,
    IntegrityError,
    OperationalError,
    ProgrammingError,
)
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine import SessionLocal, baseModel

# 本模块方法
from ..exceptions import BaseHttpException
from .convert_exception import _convert_db_exception
from .single_worker import SingleWorker
from .unit_worker import UnitWorker


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


async def get_single_worker(db: AsyncSession, model_type: type[baseModel]) -> SingleWorker:
    return SingleWorker(db, model_type)


# 依赖注入
async def get_unit_worker(db: AsyncSession = Depends(get_db)) -> UnitWorker:
    return UnitWorker(db)

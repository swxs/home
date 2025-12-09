from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine import SessionLocal, baseModel
from mysqlengine.repositories.single_worker import SingleWorker
from mysqlengine.repositories.unit_worker import UnitWorker


async def get_db():
    async with SessionLocal() as session:
        yield session


async def get_single_worker(db: AsyncSession, model_type: type[baseModel]) -> SingleWorker:
    return SingleWorker(db, model_type)


# 依赖注入
async def get_unit_worker(db: AsyncSession = Depends(get_db)) -> UnitWorker:
    return UnitWorker(db)

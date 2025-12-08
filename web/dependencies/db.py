from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine import SessionLocal
from mysqlengine.repositories.unit_worker import UnitWorker


async def get_db():
    async with SessionLocal() as session:
        yield session


# 依赖注入
async def get_unit_worker(db: AsyncSession = Depends(get_db)) -> UnitWorker:
    return UnitWorker(db)

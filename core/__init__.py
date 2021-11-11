from . import config
from . import path
from . import logger

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from umongo.frameworks import MotorAsyncIOInstance


class DataBase:
    client: AsyncIOMotorClient = None


mongodb_database = DataBase()


def get_database() -> AsyncIOMotorDatabase:
    if mongodb_database.client:
        return mongodb_database.client[config.MONGODB_DBNAME]
    return AsyncIOMotorClient(config.MONGODB_URI)[config.MONGODB_DBNAME]


def get_client() -> AsyncIOMotorClient:
    if not mongodb_database.client:
        return AsyncIOMotorClient(config.MONGODB_URI)
    return mongodb_database.client


mongodb_db = get_database()
mongodb_instance = MotorAsyncIOInstance(mongodb_db)

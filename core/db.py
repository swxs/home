from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from umongo.frameworks import MotorAsyncIOInstance
from . import config


class DataBase:
    client: AsyncIOMotorClient = None


database = DataBase()


def get_database() -> AsyncIOMotorDatabase:
    if database.client:
        return database.client[config.MONGODB_DBNAME]
    return AsyncIOMotorClient(config.MONGODB_URI)[config.MONGODB_DBNAME]


def get_client() -> AsyncIOMotorClient:
    if not database.client:
        return AsyncIOMotorClient(config.MONGODB_URI)
    return database.client


db = get_database()
instance = MotorAsyncIOInstance(db)


def connect_db_mysql():
    import asyncio
    import pymysql

    pymysql.install_as_MySQLdb()

    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy import Column, Integer, String, Text, MetaData, Table
    from sqlalchemy.schema import CreateTable
    from sqlalchemy.orm import sessionmaker

    from sqlalchemy_aio import ASYNCIO_STRATEGY, TRIO_STRATEGY
    from sqlalchemy_aio.asyncio import AsyncioEngine

    engine = create_engine(
        "mysql://root:swxs@localhost/runoob", strategy=ASYNCIO_STRATEGY, encoding='latin1', echo=False
    )
    return engine


try:
    MYSQL_INSTANCE = connect_db_mysql()
    print("mongo db connect success!")
except Exception as e:
    MYSQL_INSTANCE = None
    print("mysql db connect failed!")

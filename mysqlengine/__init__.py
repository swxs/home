from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from bson import ObjectId
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import delete, func, select
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

from core import config
from mysqlengine.fields import ObjectIdType
from web.custom_types import objectId
from web.dependencies.pagination import PageSchema, PaginationSchema
from web.exceptions import Http400BadRequestException

# 创建一个 SQLAlchemy的"引擎"
engine = create_async_engine(
    config.MYSQL_URL,
    pool_size=config.MYSQL_POOL_SIZE,
    max_overflow=100,
    pool_recycle=3600,
    pool_timeout=10,
    echo=False,
)

# SessionLocal该类的每个实例将是一个数据库会话。该类本身还不是数据库会话。
# 一旦我们创建了SessionLocal该类的实例，该实例将成为实际的数据库会话。
# 对于异步会话，需要使用 async_sessionmaker 而不是 sessionmaker
SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# 我们将用这个类继承，来创建每个数据库模型或类（ORM 模型）
Base = declarative_base()


class baseModel(Base):
    # 定义为抽象类，只能被继承，不能实例化
    __abstract__ = True
    # 默认字段
    id: Mapped[objectId] = mapped_column(
        ObjectIdType,
        primary_key=True,
        default=ObjectId,
        comment="主键ID",
    )
    create_by: Mapped[Optional[str]] = mapped_column(
        ObjectIdType,
        nullable=True,
        comment="创建用户",
    )
    create_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6),
        default=datetime.now,
        comment="创建时间",
    )
    update_by: Mapped[Optional[str]] = mapped_column(
        ObjectIdType,
        nullable=True,
        comment="更新用户",
    )
    update_at: Mapped[datetime] = mapped_column(
        DATETIME(fsp=6),
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间",
    )
    delete_at: Mapped[Optional[datetime]] = mapped_column(
        DATETIME(fsp=6),
        nullable=True,
        comment="删除时间",
    )

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

    @classmethod
    async def find_one(
        cls,
        db: AsyncSession,
        id: str,
        error_message: str = "资源不存在",
    ):
        """
        根据ID查找单个资源

        Args:
            db: 数据库会话
            id: 资源ID
            error_message: 资源不存在时的错误消息

        Returns:
            找到的资源实例

        Raises:
            Http400BadRequestException: 资源不存在时抛出
        """
        query = select(cls).where(cls.id == id)
        result = await db.execute(query)
        instance = result.scalar_one_or_none()

        if instance is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, error_message)

        return instance

    @classmethod
    async def search(
        cls,
        db: AsyncSession,
        schema: PydanticBaseModel,
        page_schema: PageSchema,
    ) -> Dict[str, Any]:
        """
        搜索资源列表（支持过滤、排序、分页）

        Args:
            schema: 过滤条件的Schema对象
            page_schema: 分页Schema对象
            db: 数据库会话

        Returns:
            包含data和pagination的字典
        """
        # 构建查询条件
        query = select(cls)
        count_query = select(func.count()).select_from(cls)

        # 应用过滤条件
        filter_dict = schema.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in filter_dict.items():
            if hasattr(cls, key):
                query = query.where(getattr(cls, key) == value)
                count_query = count_query.where(getattr(cls, key) == value)

        # 应用排序
        if page_schema.order_by:
            for order_field in page_schema.order_by:
                if hasattr(cls, order_field):
                    query = query.order_by(getattr(cls, order_field))

        # 应用分页
        if page_schema.use_pager and page_schema.limit > 0:
            query = query.offset(page_schema.skip).limit(page_schema.limit)

        # 执行查询
        result = await db.execute(query)
        instances = result.scalars().all()

        # 获取总数
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0

        # 构建分页信息
        pagination = PaginationSchema(
            total=total,
            order_by=page_schema.order_by,
            use_pager=page_schema.use_pager,
            page=page_schema.page,
            page_number=page_schema.page_number,
        )

        return {
            "data": instances,
            "pagination": pagination,
        }

    @classmethod
    async def create_one(
        cls,
        db: AsyncSession,
        schema: PydanticBaseModel,
        error_message: str = "创建失败",
    ):
        """
        创建单个资源

        Args:
            schema: 资源数据的Schema对象
            db: 数据库会话
            error_message: 创建失败时的错误消息

        Returns:
            创建的资源实例

        Raises:
            Http400BadRequestException: 创建失败时抛出
        """
        instance = cls(**schema.model_dump())
        db.add(instance)
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise Http400BadRequestException(Http400BadRequestException.IllegalArgument, error_message)
        await db.refresh(instance)

        return instance

    @classmethod
    async def update_one(
        cls,
        db: AsyncSession,
        id: str,
        schema: PydanticBaseModel,
        error_message_not_found: str = "资源不存在",
        error_message_update: str = "更新失败",
    ):
        """
        更新单个资源

        Args:
            id: 资源ID
            schema: 更新数据的Schema对象
            db: 数据库会话
            error_message_not_found: 资源不存在时的错误消息
            error_message_update: 更新失败时的错误消息

        Returns:
            更新后的资源实例

        Raises:
            Http400BadRequestException: 资源不存在或更新失败时抛出
        """
        # 查询资源
        instance = await cls.find_one(id, db, error_message_not_found)

        # 更新资源信息
        update_data = schema.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            raise Http400BadRequestException(Http400BadRequestException.IllegalArgument, error_message_update)
        await db.refresh(instance)

        return instance

    @classmethod
    async def delete_one(
        cls,
        id: str,
        db: AsyncSession,
        error_message_not_found: str = "资源不存在",
        error_message_delete: str = "删除失败",
    ) -> int:
        """
        删除单个资源

        Args:
            id: 资源ID
            db: 数据库会话
            error_message_not_found: 资源不存在时的错误消息
            error_message_delete: 删除失败时的错误消息

        Returns:
            删除的行数

        Raises:
            Http400BadRequestException: 资源不存在或删除失败时抛出
        """
        # 查询资源（验证存在性）
        await cls.find_one(id, db, error_message_not_found)

        # 删除资源
        try:
            stmt = delete(cls).where(cls.id == id)
            result = await db.execute(stmt)
            await db.commit()
            count = result.rowcount
        except Exception as e:
            await db.rollback()
            raise Http400BadRequestException(Http400BadRequestException.IllegalArgument, error_message_delete)

        return count

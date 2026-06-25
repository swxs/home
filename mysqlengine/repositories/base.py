# -*- coding: utf-8 -*-
# @File    : repositories/base.py
# @AUTH    : code_creater

from typing import Any, Dict, Generic, Optional, Type, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine import baseModel
from web.exceptions import Http400BadRequestException
from web.schemas.pagination import PageSchema, PaginationSchema

T = TypeVar("T", bound=baseModel)


class BaseRepository(Generic[T]):
    """
    通用Repository基类
    不依赖具体表结构，通过Generic和反射实现
    """

    def __init__(self, model: Type[T], db: AsyncSession):
        """
        初始化Repository

        Args:
            model: 模型类（如User, UserAuth）
            db: 数据库会话
        """
        self.db = db
        self.model = model

    async def find_one(self, id: str) -> Optional[T]:
        """
        根据ID查找单个资源

        Args:
            id: 资源ID
            error_message: 资源不存在时的错误消息

        Returns:
            找到的资源实例

        Raises:
            Http400BadRequestException: 资源不存在时抛出
        """
        query = select(self.model).where(self.model.id == id)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def find_one_or_none(self, schema: PydanticBaseModel) -> Optional[T]:
        """
        根据ID查找单个资源，不存在返回None

        Args:
            id: 资源ID

        Returns:
            找到的资源实例或None
        """
        query = select(self.model)
        filter_dict = schema.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in filter_dict.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    def _apply_schema_filters(self, query, count_query, schema: PydanticBaseModel):
        """
        将 schema 的字段作为等值过滤条件应用到 query 与 count_query。
        通过反射，不依赖具体表字段。子类可复用。
        """
        filter_dict = schema.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in filter_dict.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
                count_query = count_query.where(getattr(self.model, key) == value)
        return query, count_query

    def _apply_pagination(self, query, page_schema: PageSchema):
        """应用分页（offset/limit）。子类可复用。"""
        if page_schema.use_pager and page_schema.limit > 0:
            query = query.offset(page_schema.skip).limit(page_schema.limit)
        return query

    def _build_pagination(self, total: int, page_schema: PageSchema) -> PaginationSchema:
        """构建分页信息。子类可复用（含自定义 join/行查询场景）。"""
        return PaginationSchema(
            total=total,
            order_by=page_schema.order_by,
            use_pager=page_schema.use_pager,
            page=page_schema.page,
            page_number=page_schema.page_number,
        )

    async def _paginate_result(self, query, count_query, page_schema: PageSchema) -> Dict[str, Any]:
        """执行查询与计数，构建统一的 {data, pagination} 返回。子类可复用。"""
        result = await self.db.execute(query)
        instances = result.scalars().all()

        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        return {
            "data": instances,
            "pagination": self._build_pagination(total, page_schema),
        }

    async def search(
        self,
        schema: PydanticBaseModel,
        page_schema: PageSchema,
    ) -> Dict[str, Any]:
        """
        搜索资源列表（支持过滤、排序、分页）
        不依赖具体表结构，通过反射动态构建查询

        Args:
            schema: 过滤条件的Schema对象
            page_schema: 分页Schema对象

        Returns:
            包含data和pagination的字典
        """
        # 构建查询条件
        query = select(self.model)
        count_query = select(func.count()).select_from(self.model)

        # 应用过滤条件（通过反射，不依赖具体字段）
        query, count_query = self._apply_schema_filters(query, count_query, schema)

        # 应用排序（通过反射）
        if page_schema.order_by:
            for order_field in page_schema.order_by:
                if hasattr(self.model, order_field):
                    query = query.order_by(getattr(self.model, order_field))

        # 应用分页
        query = self._apply_pagination(query, page_schema)

        return await self._paginate_result(query, count_query, page_schema)

    async def create_one(
        self,
        schema: PydanticBaseModel,
    ) -> T:
        """
        创建单个资源
        不依赖具体表结构，通过schema动态创建实例

        Args:
            schema: 资源数据的Schema对象

        Returns:
            创建的资源实例
        """
        instance = self.model(**schema.model_dump())
        self.db.add(instance)
        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def update_one(
        self,
        id: str,
        schema: PydanticBaseModel,
    ) -> T:
        """
        更新单个资源
        不依赖具体表结构，通过反射动态更新字段

        Args:
            id: 资源ID
            schema: 更新数据的Schema对象

        Returns:
            更新后的资源实例

        Raises:
            Http400BadRequestException: 资源不存在或更新失败时抛出
        """
        # 查询资源
        instance = await self.find_one(id)

        if not instance:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "对象不存在")

        # 更新资源信息（通过反射，不依赖具体字段）
        update_data = schema.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in update_data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        await self.db.flush()
        await self.db.refresh(instance)
        return instance

    async def delete_one(
        self,
        id: str,
    ):
        """
        删除单个资源
        不依赖具体表结构，通过Generic实现

        Args:
            id: 资源ID

        Returns:
            删除的行数
        """
        stmt = delete(self.model).where(self.model.id == id)
        result = await self.db.execute(stmt)
        await self.db.flush()
        return result.rowcount

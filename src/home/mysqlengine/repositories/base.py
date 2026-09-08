# -*- coding: utf-8 -*-
# @File    : repositories/base.py
# @AUTH    : code_creater

from typing import Any, ClassVar, Dict, Generic, Optional, Set, Tuple, Type, TypeVar

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import Select, delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from home.mysqlengine import baseModel
from home.web.exceptions import Http400BadRequestException
from home.web.schemas.pagination import PageSchema, PaginationSchema

T = TypeVar("T", bound=baseModel)


class BaseRepository(Generic[T]):
    """
    通用Repository基类
    不依赖具体表结构，通过 Generic 与反射实现「过滤 / 排序 / 分页 / 查询构建」四段可组合原语。

    子类约定：
    - 以类属性声明绑定模型与白名单::

        class UserRepository(BaseRepository[User]):
            model = User
            filterable_fields = {"username"}
            sortable_fields = {"id", "create_at", "username"}

    - 需要 join / 聚合等自定义查询时，只覆盖 ``build_query``；过滤 / 排序 / 分页由基类统一处理。
    - 返回 join 多实体行（非单一 ORM）时，置 ``returns_scalars = False``。
    - 统一返回 ``{"data": [...], "pagination": PaginationSchema}``；DTO 转换在 service 层。

    安全基线：``filterable_fields`` / ``sortable_fields`` 为 None 时分别拒绝过滤 / 排序，
    避免任意列（如 credential）被外部用于过滤或排序。
    """

    model: Type[T]
    # 白名单：None 表示拒绝（不允许该能力作用于任何字段）。
    sortable_fields: ClassVar[Optional[Set[str]]] = None
    filterable_fields: ClassVar[Optional[Set[str]]] = None
    # search() 默认返回单一 ORM（scalars）；join 多实体场景置 False 返回 Row 元组。
    returns_scalars: ClassVar[bool] = True

    def __init__(self, session: AsyncSession):
        """
        初始化Repository

        Args:
            session: 数据库会话
        """
        self.session = session

    async def find_one(self, id: str) -> Optional[T]:
        """
        根据ID查找单个资源

        Args:
            id: 资源ID

        Returns:
            找到的资源实例或None
        """
        query = select(self.model).where(self.model.id == id)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_one_or_none(self, schema: PydanticBaseModel) -> Optional[T]:
        """
        根据schema字段精确匹配查找单个资源，不存在返回None。

        说明：单条精确查找，按 schema 已声明字段反射匹配，不走列表白名单。
        """
        query = select(self.model)
        filter_dict = schema.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in filter_dict.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)

        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    # ------------------------------------------------------------------
    # 可组合原语：过滤 / 排序 / 分页 / 查询构建
    # ------------------------------------------------------------------
    def _apply_filters(self, query, count_query, filters: Dict[str, Any]):
        """按 ``filterable_fields`` 白名单做等值过滤，同时作用于 query 与 count_query。

        未声明（None）或不在白名单中的字段一律忽略（安全基线）。
        """
        if not self.filterable_fields:
            return query, count_query
        for key, value in filters.items():
            if key not in self.filterable_fields:
                continue
            col = getattr(self.model, key, None)
            if col is None:
                continue
            query = query.where(col == value)
            count_query = count_query.where(col == value)
        return query, count_query

    def _apply_ordering(self, query, page_schema: PageSchema):
        """按 ``sortable_fields`` 白名单排序，支持 ``-`` 前缀降序。

        未声明（None）或不在白名单中的字段一律忽略（安全基线，同时修复历史上 ``-`` 前缀被静默丢弃的问题）。
        """
        if not self.sortable_fields:
            return query
        for raw in page_schema.order_by or []:
            descending = raw.startswith("-")
            field = raw[1:] if descending else raw
            if field not in self.sortable_fields:
                continue
            col = getattr(self.model, field, None)
            if col is None:
                continue
            query = query.order_by(col.desc() if descending else col.asc())
        return query

    def _apply_pagination(self, query, page_schema: PageSchema):
        """应用分页（offset/limit）。子类可复用。"""
        if page_schema.use_pager and page_schema.limit > 0:
            query = query.offset(page_schema.skip).limit(page_schema.limit)
        return query

    def _build_pagination(self, total: int, page_schema: PageSchema) -> PaginationSchema:
        """构建分页信息。子类可复用（含自定义 join/行查询场景）。"""
        return PaginationSchema(
            total=total,
            use_pager=page_schema.use_pager,
            page=page_schema.page,
            page_number=page_schema.page_number,
        )

    def build_query(self, filters: Dict[str, Any]) -> Tuple[Select, Select]:  # pylint: disable=unused-argument
        """构建 (数据查询, 计数查询)。默认单表；子类覆盖以实现 join / 聚合 / 附加列。

        过滤 / 排序 / 分页由基类统一在 ``search`` 中应用，无需在此重复。
        ``filters`` 供子类按需取用（如 join 条件），默认实现不需要。
        """
        return (
            select(self.model),
            select(func.count()).select_from(self.model),
        )

    async def paginate(
        self,
        query,
        count_query,
        page_schema: PageSchema,
        *,
        scalars: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """执行计数与分页查询，构建统一的 {data, pagination} 返回。

        Args:
            scalars: True 返回单一 ORM 列表；False 返回 Row 元组列表；None 取 ``returns_scalars``。
        """
        use_scalars = self.returns_scalars if scalars is None else scalars

        total = (await self.session.execute(count_query)).scalar() or 0
        query = self._apply_pagination(query, page_schema)
        result = await self.session.execute(query)
        data = result.scalars().all() if use_scalars else result.all()

        return {
            "data": list(data),
            "pagination": self._build_pagination(total, page_schema),
        }

    async def search(
        self,
        schema: PydanticBaseModel,
        page_schema: PageSchema,
    ) -> Dict[str, Any]:
        """搜索资源列表（过滤 / 排序 / 分页），通过组合原语实现。

        自定义查询请覆盖 ``build_query``，本方法的编排（过滤/排序/分页）保持不变。

        Returns:
            包含 data 和 pagination 的字典
        """
        filters = schema.model_dump(exclude_unset=True, exclude_none=True)
        query, count_query = self.build_query(filters)
        query, count_query = self._apply_filters(query, count_query, filters)
        query = self._apply_ordering(query, page_schema)
        return await self.paginate(query, count_query, page_schema)

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
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
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

        await self.session.flush()
        await self.session.refresh(instance)
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
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.rowcount

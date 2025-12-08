# -*- coding: utf-8 -*-
# @File    : repositories/password_lock_repository.py
# @AUTH    : code_creater

from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import contains_eager

from mysqlengine.repositories import BaseRepository
from web.dependencies.pagination import PageSchema, PaginationSchema

# 本模块方法
from ..models.password_lock import PasswordLock


class PasswordLockRepository(BaseRepository[PasswordLock]):
    """
    密码锁Repository
    可以在这里添加PasswordLock特定的查询方法
    """

    name = "PasswordLock"

    def __init__(self, db: AsyncSession):
        super().__init__(PasswordLock, db)

    async def search_with_name_like(
        self,
        schema: PydanticBaseModel,
        page_schema: PageSchema,
        name_search: Optional[str] = None,
    ):
        """
        搜索密码锁列表，支持名称模糊搜索
        """
        # 构建查询条件
        query = select(PasswordLock)
        count_query = select(func.count()).select_from(PasswordLock)

        # 应用过滤条件
        filter_dict = schema.model_dump(exclude_unset=True, exclude_none=True)
        for key, value in filter_dict.items():
            if hasattr(PasswordLock, key):
                query = query.where(getattr(PasswordLock, key) == value)
                count_query = count_query.where(getattr(PasswordLock, key) == value)

        # 应用名称模糊搜索
        if name_search:
            query = query.where(
                or_(
                    PasswordLock.name.like(f"%{name_search}%"),
                    PasswordLock.website.like(f"%{name_search}%"),
                )
            )
            count_query = count_query.where(
                or_(
                    PasswordLock.name.like(f"%{name_search}%"),
                    PasswordLock.website.like(f"%{name_search}%"),
                )
            )

        # 应用排序
        if page_schema.order_by:
            for order_field in page_schema.order_by:
                if hasattr(PasswordLock, order_field):
                    query = query.order_by(getattr(PasswordLock, order_field))

        # 应用分页
        if page_schema.use_pager and page_schema.limit > 0:
            query = query.offset(page_schema.skip).limit(page_schema.limit)

        # 执行查询
        result = await self.db.execute(query)
        instances = result.scalars().all()

        # 获取总数
        count_result = await self.db.execute(count_query)
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

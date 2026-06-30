# -*- coding: utf-8 -*-
# @File    : repositories/password_lock_repository.py
# @AUTH    : code_creater

from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import func, or_, select

from mysqlengine.repositories import BaseRepository
from web.schemas.pagination import PageSchema

# 本模块方法
from ..models.password_lock import PasswordLock


class PasswordLockRepository(BaseRepository[PasswordLock]):
    """
    密码锁Repository
    可以在这里添加PasswordLock特定的查询方法
    """

    model = PasswordLock
    name = "password_lock"

    async def search_with_name_like(
        self,
        schema: PydanticBaseModel,
        page_schema: PageSchema,
        name_search: Optional[str] = None,
    ):
        """
        搜索密码锁列表，支持名称模糊搜索
        """
        query = select(PasswordLock)
        count_query = select(func.count()).select_from(PasswordLock)

        # 应用等值过滤条件（复用基类逻辑）
        query, count_query = self._apply_schema_filters(query, count_query, schema)

        # 应用名称模糊搜索
        if name_search:
            like_clause = or_(
                PasswordLock.name.like(f"%{name_search}%"),
                PasswordLock.website.like(f"%{name_search}%"),
            )
            query = query.where(like_clause)
            count_query = count_query.where(like_clause)

        # 应用排序（支持 "-" 前缀降序）
        if page_schema.order_by:
            for order_field in page_schema.order_by:
                if order_field.startswith("-"):
                    _order_field = order_field[1:]
                    if hasattr(PasswordLock, _order_field):
                        query = query.order_by(getattr(PasswordLock, _order_field).desc())
                else:
                    _order_field = order_field
                    if hasattr(PasswordLock, _order_field):
                        query = query.order_by(getattr(PasswordLock, _order_field).asc())

        # 应用分页（复用基类逻辑）
        query = self._apply_pagination(query, page_schema)

        return await self._paginate_result(query, count_query, page_schema)

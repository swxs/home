# -*- coding: utf-8 -*-
# @File    : repositories/password_lock_repository.py
# @AUTH    : code_creater

from typing import Optional

from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import or_

from home.mysqlengine.repositories import BaseRepository
from home.web.schemas.pagination import PageSchema

# 本模块方法
from ..models.password_lock import PasswordLock


class PasswordLockRepository(BaseRepository[PasswordLock]):
    """
    密码锁Repository
    可以在这里添加PasswordLock特定的查询方法
    """

    model = PasswordLock
    name = "password_lock"

    filterable_fields = {"user_id", "name", "key", "website", "used", "ttype"}
    # custom(JSON) 不入排序白名单
    sortable_fields = {"id", "create_at", "update_at", "name", "website", "used"}

    async def search_with_name_like(
        self,
        schema: PydanticBaseModel,
        page_schema: PageSchema,
        name_search: Optional[str] = None,
    ):
        """搜索密码锁列表，在等值过滤之上叠加 name/website 跨字段模糊搜索。

        过滤 / 排序 / 分页复用基类原语；模糊搜索为本方法专有逻辑。
        """
        filters = schema.model_dump(exclude_unset=True, exclude_none=True)
        query, count_query = self.build_query(filters)

        # 白名单等值过滤（复用基类）
        query, count_query = self._apply_filters(query, count_query, filters)

        # name / website 跨字段模糊搜索（本方法专有）
        if name_search:
            like_clause = or_(
                PasswordLock.name.like(f"%{name_search}%"),
                PasswordLock.website.like(f"%{name_search}%"),
            )
            query = query.where(like_clause)
            count_query = count_query.where(like_clause)

        # 排序（复用基类，支持 - 前缀降序 + 白名单）
        query = self._apply_ordering(query, page_schema)

        return await self.paginate(query, count_query, page_schema)

# -*- coding: utf-8 -*-
# @File    : repositories/user_search_repository.py
# @AUTH    : code_creater

"""聚合查询 Repository：分页查询 user，并在 SQL 层把认证信息拍平为字段。

实现方式：继承 ``BaseRepository[User]``，覆盖 ``build_query`` 把每个拍平字段做成
相关聚合子查询 ``MAX(UserAuth.identifier)``（按 ttype）内联到 user 查询，单条 SQL
即完成「分页 user + 拍平认证」；过滤 / 排序 / 分页全部复用基类原语。

- ``returns_scalars = False``：查询返回 (User, phone, email...) 行；
- 每个用户取对应 ttype 认证的 identifier，无认证则为 NULL（=> None）；分页落在 user 上，行数不被认证放大；
- ``search_with_auth`` 为薄封装：把 Row 重塑为 (User, {拍平字段}) 供 service 做 DTO 转换。
只读聚合在同一 session 内查询天然一致，无需事务包装。
"""

from typing import Any, Dict, List, Tuple

from sqlalchemy import func, select

from mysqlengine.repositories import BaseRepository
from web.schemas.pagination import PageSchema, PaginationSchema

# 本模块方法
from .. import consts
from ..models.user import User
from ..models.user_auth import UserAuth
from ..schemas.user import UserFilter

# 拍平字段名 -> 对应认证类型（取该类型认证的 identifier）。
# 新增可暴露字段时，这里与 UserWithAuthOut 同步加一行即可。
_FLATTEN_FIELDS: Dict[str, consts.UserAuth_Ttype] = {
    "phone": consts.UserAuth_Ttype.PHONE,
    "email": consts.UserAuth_Ttype.EMAIL,
}


class UserSearchRepository(BaseRepository[User]):
    """User 聚合查询：单条 SQL 返回 user + 拍平认证字段。"""

    model = User
    name = "user_search"

    filterable_fields = {"username", "description", "avatar"}
    sortable_fields = {"id", "create_at", "update_at", "username"}
    # build_query 附带拍平列，查询返回 Row 而非单一 ORM
    returns_scalars = False

    @staticmethod
    def _flat_col(ttype: consts.UserAuth_Ttype, name: str):
        """某 ttype 认证的代表 identifier（相关聚合子查询，无认证为 NULL）。"""
        return (
            select(func.max(UserAuth.identifier))
            .where(UserAuth.user_id == User.id, UserAuth.ttype == ttype)
            .correlate(User)
            .scalar_subquery()
            .label(name)
        )

    def build_query(self, filters: Dict[str, Any]):
        flat = [self._flat_col(ttype, name) for name, ttype in _FLATTEN_FIELDS.items()]
        return (
            select(User, *flat),
            select(func.count()).select_from(User),
        )

    async def search_with_auth(
        self,
        user_filter: UserFilter,
        page_schema: PageSchema,
    ) -> Tuple[List[Tuple[User, Dict[str, Any]]], PaginationSchema]:
        """分页查询 user，并附带其拍平后的认证字段。"""
        result = await self.search(user_filter, page_schema)
        rows = [
            (row[0], {name: row._mapping[name] for name in _FLATTEN_FIELDS})
            for row in result["data"]
        ]
        return rows, result["pagination"]

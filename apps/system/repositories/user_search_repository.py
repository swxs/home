# -*- coding: utf-8 -*-
# @File    : repositories/user_search_repository.py
# @AUTH    : code_creater

"""聚合查询 Repository：分页查询 user，并在 SQL 层把认证信息拍平为字段。

与表级 Repository（BaseRepository[T]，绑定单一 ORM 模型）不同，聚合 Repository
跨多表取数、不继承 BaseRepository；通过 Repo(db) 复用表级 Repository 的分页能力。

取数策略：
1. 复用 UserRepository.search 做过滤 / 排序 / 分页（分页落在 user 上，行数不被认证放大）；
2. 对该页 user_id 用一次条件聚合（GROUP BY user_id）把不同 ttype 的认证拍平为
   phone / email 等字段；同一用户同类型多条时取聚合后的一条。
返回 (user, 拍平字段 dict) 列表 —— 不再返回原始认证列表，DTO 转换交给 service。
只读聚合在同一 session 内查询天然一致，无需事务包装。
"""

from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy import case, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from web.schemas.pagination import PageSchema, PaginationSchema

# 本模块方法
from .. import consts
from ..models.user import User
from ..models.user_auth import UserAuth
from ..schemas.user import UserFilter
from .user_repository import UserRepository

# 拍平字段名 -> 对应认证类型（取该类型认证的 identifier）。
# 新增可暴露字段时，这里与 UserWithAuthOut 同步加一行即可。
_FLATTEN_FIELDS: Dict[str, consts.UserAuth_Ttype] = {
    "phone": consts.UserAuth_Ttype.PHONE,
    "email": consts.UserAuth_Ttype.EMAIL,
}


class UserSearchRepository:
    """User 聚合查询：返回 (User, 拍平字段) 与分页信息。"""

    def __init__(self, db: AsyncSession, user_repo: Optional[UserRepository] = None):
        self.db = db
        self.user_repo = user_repo or UserRepository(db)

    async def _flatten_auth(self, user_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """按 user_id 把认证拍平为 {user_id: {phone, email, ...}}。"""
        if not user_ids:
            return {}

        flat_cols = [
            func.max(case((UserAuth.ttype == ttype, UserAuth.identifier))).label(name)
            for name, ttype in _FLATTEN_FIELDS.items()
        ]
        query = (
            select(UserAuth.user_id.label("user_id"), *flat_cols)
            .where(UserAuth.user_id.in_(user_ids))
            .group_by(UserAuth.user_id)
        )
        result = await self.db.execute(query)

        flat_map: Dict[str, Dict[str, Any]] = {}
        for row in result.all():
            mapping = row._mapping
            flat_map[str(mapping["user_id"])] = {
                name: mapping[name] for name in _FLATTEN_FIELDS
            }
        return flat_map

    async def search_with_auth(
        self,
        user_filter: UserFilter,
        page_schema: PageSchema,
    ) -> Tuple[List[Tuple[User, Dict[str, Any]]], PaginationSchema]:
        """分页查询 user，并附带其拍平后的认证字段。"""
        result = await self.user_repo.search(user_filter, page_schema)
        user_list: List[User] = result["data"]
        pagination: PaginationSchema = result["pagination"]

        user_ids = [str(user.id) for user in user_list]
        flat_map = await self._flatten_auth(user_ids)

        empty = {name: None for name in _FLATTEN_FIELDS}
        rows = [(user, flat_map.get(str(user.id), empty)) for user in user_list]
        return rows, pagination

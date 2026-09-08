# -*- coding: utf-8 -*-
# @File    : services/user_searcher_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict, List, Optional

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from home.web.dependencies.db import get_db
from home.web.schemas.pagination import PageSchema

# 本模块方法
from ..repositories.user_search_repository import UserSearchRepository
from ..schemas.user import UserFilter, UserSchema

logger = logging.getLogger("main.apps.system.services.user_searcher_service")


class UserSearcherService:
    """用户聚合查询业务层：编排 User 与 UserAuth 的关联查询。

    取数委托给 UserSearchRepository（返回 ORM）；合并与 DTO 转换在 service 内完成。
    只读路径不使用事务（同一 session 内多次查询天然一致）。search_repo 可选注入便于单测。

    注意：保留现有 /self 行为（未按 token 的 user_id 过滤），归属授权问题仅标注不修复。
    """

    def __init__(
        self,
        db: AsyncSession,
        search_repo: Optional[UserSearchRepository] = None,
    ):
        self.db = db
        self.search_repo = search_repo or UserSearchRepository(db)

    async def list_self(self, user_schema: UserFilter, page_schema: PageSchema) -> Dict[str, Any]:
        rows, pagination = await self.search_repo.search_with_auth(user_schema, page_schema)

        # repo 已在 SQL 层把认证拍平为字段（phone / email ...），service 只做 DTO 拼接
        data: List[Dict[str, Any]] = []
        for user, flat in rows:
            user_data = UserSchema.model_validate(user).model_dump()
            user_data.update(flat)
            data.append(user_data)

        return {
            "data": data,
            "pagination": pagination.model_dump(),
        }


async def get_user_searcher_service(db: AsyncSession = Depends(get_db)) -> UserSearcherService:
    return UserSearcherService(db)

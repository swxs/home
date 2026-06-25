# -*- coding: utf-8 -*-
# @File    : services/user_searcher_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db
from web.dependencies.unit_worker import UnitWorker
from web.schemas.pagination import PageSchema

# 本模块方法
from ..models.user import User
from ..models.user_auth import UserAuth
from ..repositories.user_auth_repository import UserAuthRepository
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserFilter, UserSchema
from ..schemas.user_auth import UserAuthSchema

logger = logging.getLogger("main.apps.system.services.user_searcher_service")


class UserSearcherService:
    """用户聚合查询业务层：User 与 UserAuth 关联查询。

    注意：保留现有 /self 行为（未按 token 的 user_id 过滤），归属授权问题仅标注不修复。
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_self(self, user_schema: UserFilter, page_schema: PageSchema) -> Dict[str, Any]:
        unit_worker = UnitWorker(self.db)
        async with unit_worker as uw:
            user_repo: UserRepository = uw.get_repository(User)
            user_auth_repo: UserAuthRepository = uw.get_repository(UserAuth)

            # 使用Repository搜索方法
            result = await user_repo.search(user_schema, page_schema)
            user_list = result["data"]

            # 获取用户ID列表
            user_ids = [str(user.id) for user in user_list]

            # 使用Repository查找UserAuth
            if user_ids:
                user_auth_list = await user_auth_repo.find_by_user_ids(user_ids)
            else:
                user_auth_list = []

            # 构建用户认证信息字典
            infos = {
                str(user_auth.user_id): {"user_auth": UserAuthSchema.model_validate(user_auth).model_dump()}
                for user_auth in user_auth_list
            }

            # 转换为 Schema 并合并用户和认证信息
            user_data_list = []
            for user in user_list:
                user_data = UserSchema.model_validate(user).model_dump()
                user_data.update(infos.get(str(user.id), {}))
                user_data_list.append(user_data)

        return {
            "data": user_data_list,
            "pagination": result["pagination"].model_dump(),
        }


async def get_user_searcher_service(db: AsyncSession = Depends(get_db)) -> UserSearcherService:
    return UserSearcherService(db)

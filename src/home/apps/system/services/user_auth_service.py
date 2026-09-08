# -*- coding: utf-8 -*-
# @File    : services/user_auth_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict, Optional

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from home.web.dependencies.db import get_db
from home.web.dependencies.transaction import transaction
from home.web.exceptions import Http400BadRequestException
from home.web.schemas.pagination import PageSchema

# 本模块方法
from ..repositories.user_auth_repository import UserAuthRepository
from ..schemas.user_auth import (
    UserAuthCreate,
    UserAuthFilter,
    UserAuthOut,
    UserAuthUpdate,
)

logger = logging.getLogger("main.apps.system.services.user_auth_service")


class UserAuthService:
    """用户认证业务层：CRUD 编排与事务边界。"""

    def __init__(self, db: AsyncSession, repo: Optional[UserAuthRepository] = None):
        self.db = db
        self.repo = repo or UserAuthRepository(db)

    async def list(self, filter_schema: UserAuthFilter, page_schema: PageSchema) -> Dict[str, Any]:
        result = await self.repo.search(filter_schema, page_schema)

        return {
            "data": [UserAuthOut.model_validate(user_auth) for user_auth in result["data"]],
            "pagination": result["pagination"],
        }

    async def get(self, user_auth_id: str) -> UserAuthOut:
        user_auth = await self.repo.find_one(user_auth_id)

        if user_auth is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "用户认证信息不存在")

        return UserAuthOut.model_validate(user_auth)

    async def create(self, schema: UserAuthCreate) -> UserAuthOut:
        async with transaction(self.db):
            user_auth = await self.repo.create_one(schema)

        return UserAuthOut.model_validate(user_auth)

    async def update(self, user_auth_id: str, schema: UserAuthUpdate) -> UserAuthOut:
        async with transaction(self.db):
            user_auth = await self.repo.update_one(user_auth_id, schema)

        return UserAuthOut.model_validate(user_auth)

    async def delete(self, user_auth_id: str) -> int:
        async with transaction(self.db):
            count = await self.repo.delete_one(user_auth_id)

        return count


async def get_user_auth_service(db: AsyncSession = Depends(get_db)) -> UserAuthService:
    return UserAuthService(db)

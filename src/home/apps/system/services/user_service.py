# -*- coding: utf-8 -*-
# @File    : services/user_service.py
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
from ..repositories.user_repository import UserRepository
from ..schemas.user import UserCreate, UserFilter, UserOut, UserUpdate

logger = logging.getLogger("main.apps.system.services.user_service")


class UserService:
    """用户业务层：CRUD 编排与事务边界。"""

    def __init__(self, db: AsyncSession, repo: Optional[UserRepository] = None):
        self.db = db
        self.repo = repo or UserRepository(db)

    async def list(self, filter_schema: UserFilter, page_schema: PageSchema) -> Dict[str, Any]:
        result = await self.repo.search(filter_schema, page_schema)

        return {
            "data": [UserOut.model_validate(user) for user in result["data"]],
            "pagination": result["pagination"],
        }

    async def get(self, user_id: str) -> UserOut:
        user = await self.repo.find_one(user_id)

        if user is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "用户不存在")

        return UserOut.model_validate(user)

    async def create(self, schema: UserCreate) -> UserOut:
        async with transaction(self.db):
            user = await self.repo.create_one(schema)

        return UserOut.model_validate(user)

    async def update(self, user_id: str, schema: UserUpdate) -> UserOut:
        async with transaction(self.db):
            user = await self.repo.update_one(user_id, schema)

        return UserOut.model_validate(user)

    async def delete(self, user_id: str) -> int:
        async with transaction(self.db):
            count = await self.repo.delete_one(user_id)

        return count


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

# -*- coding: utf-8 -*-
# @File    : services/user_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.schemas.pagination import PageSchema

# 本模块方法
from ..models.user import User
from ..schemas.user import UserCreate, UserFilter, UserOut, UserUpdate

logger = logging.getLogger("main.apps.system.services.user_service")


class UserService:
    """用户业务层：CRUD 编排与事务边界。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, filter_schema: UserFilter, page_schema: PageSchema) -> Dict[str, Any]:
        single_worker = await get_single_worker(self.db, User)
        async with single_worker as worker:
            result = await worker.repository.search(filter_schema, page_schema)

        return {
            "data": [UserOut.model_validate(user) for user in result["data"]],
            "pagination": result["pagination"],
        }

    async def get(self, user_id: str) -> UserOut:
        single_worker = await get_single_worker(self.db, User)
        async with single_worker as worker:
            user = await worker.repository.find_one(user_id)

        if user is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "用户不存在")

        return UserOut.model_validate(user)

    async def create(self, schema: UserCreate) -> UserOut:
        single_worker = await get_single_worker(self.db, User)
        async with single_worker as worker:
            user = await worker.repository.create_one(schema)

        return UserOut.model_validate(user)

    async def update(self, user_id: str, schema: UserUpdate) -> UserOut:
        single_worker = await get_single_worker(self.db, User)
        async with single_worker as worker:
            user = await worker.repository.update_one(user_id, schema)

        return UserOut.model_validate(user)

    async def delete(self, user_id: str) -> int:
        single_worker = await get_single_worker(self.db, User)
        async with single_worker as worker:
            count = await worker.repository.delete_one(user_id)

        return count


async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(db)

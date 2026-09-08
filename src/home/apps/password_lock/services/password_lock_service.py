# -*- coding: utf-8 -*-
# @File    : services/password_lock_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict, Optional

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from home.web.schemas.types import objectId
from home.web.dependencies.session import get_session, transaction

# 通用方法
from home.commons.Helpers import encryption
from home.web.exceptions import Http400BadRequestException
from home.web.schemas.pagination import PageSchema

# 本模块方法
from .. import consts
from ..repositories.password_lock_repository import PasswordLockRepository
from ..schemas.password_lock import (
    PasswordLockCreate,
    PasswordLockFilter,
    PasswordLockOut,
    PasswordLockUpdate,
)

logger = logging.getLogger("main.apps.password_lock.services.password_lock_service")


class PasswordLockService:
    """密码锁业务层：承载业务编排、归属授权、解密策略与事务边界。"""

    def __init__(self, session: AsyncSession, repo: Optional[PasswordLockRepository] = None):
        self.session = session
        self.repo = repo or PasswordLockRepository(session)

    async def list(
        self,
        filter_schema: PasswordLockFilter,
        page_schema: PageSchema,
    ) -> Dict[str, Any]:
        result = await self.repo.search(filter_schema, page_schema)

        return {
            "data": [PasswordLockOut.model_validate(pl) for pl in result["data"]],
            "pagination": result["pagination"],
        }

    async def get(self, password_lock_id: objectId) -> PasswordLockOut:
        password_lock = await self.repo.find_one(password_lock_id)

        if password_lock is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

        return PasswordLockOut.model_validate(password_lock)

    async def create(self, schema: PasswordLockCreate) -> PasswordLockOut:
        async with transaction(self.session):
            password_lock = await self.repo.create_one(schema)

        return PasswordLockOut.model_validate(password_lock)

    async def update(self, password_lock_id: objectId, schema: PasswordLockUpdate) -> PasswordLockOut:
        async with transaction(self.session):
            password_lock = await self.repo.update_one(password_lock_id, schema)

        return PasswordLockOut.model_validate(password_lock)

    async def delete(self, password_lock_id: objectId) -> int:
        async with transaction(self.session):
            count = await self.repo.delete_one(password_lock_id)

        return count

    async def search_self(
        self,
        filter_schema: PasswordLockFilter,
        page_schema: PageSchema,
        user_id: objectId,
        name_search: Optional[str] = None,
    ) -> Dict[str, Any]:
        # 设置用户ID过滤
        filter_schema.user_id = user_id

        result = await self.repo.search_with_name_like(
            filter_schema,
            page_schema,
            name_search=name_search,
        )

        return {
            "data": [PasswordLockOut.model_validate(pl) for pl in result["data"]],
            "pagination": result["pagination"],
        }

    async def reveal_password(self, password_lock_id: objectId, user_id: objectId) -> Optional[str]:
        async with transaction(self.session):
            password_lock = await self.repo.find_one(password_lock_id)

            if password_lock is None:
                raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

            if str(password_lock.user_id) != user_id:
                raise Http400BadRequestException(Http400BadRequestException.IllegalArgument, "无权访问该密码")

            await self.repo.update_one(
                password_lock_id, PasswordLockUpdate(used=password_lock.used + 1)
            )

        # 获取密码
        password_lock_out = PasswordLockOut.model_validate(password_lock)
        return self._extract_password(password_lock_out)

    def _extract_password(self, password_lock: PasswordLockOut) -> Optional[str]:
        if password_lock.ttype == consts.PasswordLock_Ttype.COMMON:
            if password_lock.key:
                password = encryption.get_password(name=password_lock.key)
            else:
                password = None
        elif password_lock.ttype == consts.PasswordLock_Ttype.CUSTOM:
            password = password_lock.custom.get("password", None)
        else:
            password = None

        return password


async def get_password_lock_service(session: AsyncSession = Depends(get_session)) -> PasswordLockService:
    return PasswordLockService(session)

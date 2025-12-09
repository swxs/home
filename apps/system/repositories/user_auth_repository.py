# -*- coding: utf-8 -*-
# @File    : repositories/user_auth_repository.py
# @AUTH    : code_creater

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.user_auth import UserAuth


class UserAuthRepository(BaseRepository[UserAuth]):
    """
    用户认证Repository
    可以在这里添加UserAuth特定的查询方法
    """

    name = "user_auth"

    async def find_by_user_id(self, user_id: str) -> List[UserAuth]:
        """
        查找用户的所有认证方式
        这是UserAuth特定的方法，不依赖具体表结构细节
        """
        query = select(UserAuth).where(UserAuth.user_id == user_id)
        result = await self.db.execute(query)
        return list[UserAuth](result.scalars().all())

    async def find_by_ttype_and_identifier(self, ttype: int, identifier: str) -> List[UserAuth]:
        """
        根据认证类型和标识符查找
        """
        query = select(UserAuth).where(
            UserAuth.ttype == ttype,
            UserAuth.identifier == identifier,
        )
        result = await self.db.execute(query)
        return list[UserAuth](result.scalars().all())

    async def find_by_user_ids(self, user_ids: List[str]) -> List[UserAuth]:
        """
        根据用户ID列表查找认证信息
        """
        if not user_ids:
            return []
        query = select(UserAuth).where(UserAuth.user_id.in_(user_ids))
        result = await self.db.execute(query)
        return list[UserAuth](result.scalars().all())

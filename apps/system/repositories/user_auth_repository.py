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

    async def find_by_user_ids(self, user_ids: List[str]) -> List[UserAuth]:
        """
        根据用户ID列表查找认证信息
        """
        if not user_ids:
            return []
        query = select(UserAuth).where(UserAuth.user_id.in_(user_ids))
        result = await self.db.execute(query)
        return list[UserAuth](result.scalars().all())

# -*- coding: utf-8 -*-
# @File    : repositories/user_repository.py
# @AUTH    : code_creater

from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.user import User


class UserRepository(BaseRepository[User]):
    """
    用户Repository
    可以在这里添加User特定的查询方法
    """

    name = "User"

    def __init__(self, db: AsyncSession):
        super().__init__(User, db)

    # 如果需要User特定的方法，可以在这里添加
    # 例如：
    # async def find_by_username(self, username: str) -> Optional[User]:
    #     query = select(User).where(User.username == username)
    #     result = await self.db.execute(query)
    #     return result.scalar_one_or_none()

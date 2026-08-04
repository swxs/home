# -*- coding: utf-8 -*-
# @File    : repositories/file_share_link_repository.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.file_share_link import FileShareLink


class FileShareLinkRepository(BaseRepository[FileShareLink]):
    model = FileShareLink
    name = "file_share_link"

    filterable_fields = {"file_info_id", "name", "status", "create_by", "token"}
    sortable_fields = {"id", "create_at", "update_at", "name", "expires_at", "status"}

    async def find_by_token(self, token: str) -> Optional[FileShareLink]:
        query = select(self.model).where(self.model.token == token)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

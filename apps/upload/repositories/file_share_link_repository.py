# -*- coding: utf-8 -*-
# @File    : repositories/file_share_link_repository.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.file_share_link import FileShareLink
from ..consts import ShareLinkStatus


class FileShareLinkRepository(BaseRepository[FileShareLink]):
    model = FileShareLink
    name = "file_share_link"

    filterable_fields = {"file_info_id", "name", "status", "create_by", "token"}
    sortable_fields = {"id", "create_at", "update_at", "name", "expires_at", "status"}

    async def find_by_token(self, token: str) -> Optional[FileShareLink]:
        query = select(self.model).where(self.model.token == token)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def revoke_active_for_file(self, file_info_id: str) -> int:
        statement = (
            update(self.model)
            .where(
                self.model.file_info_id == file_info_id,
                self.model.status == ShareLinkStatus.ACTIVE,
            )
            .values(status=ShareLinkStatus.REVOKED)
        )
        result = await self.db.execute(statement)
        await self.db.flush()
        return result.rowcount

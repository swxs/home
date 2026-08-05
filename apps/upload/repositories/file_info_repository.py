# -*- coding: utf-8 -*-
# @File    : repositories/file_info_repository.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import func, select

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.file_info import FileInfo


class FileInfoRepository(BaseRepository[FileInfo]):
    """
    文件信息Repository
    可以在这里添加FileInfo特定的查询方法
    """

    model = FileInfo
    name = "file_info"

    filterable_fields = {"user_id", "file_id", "file_name", "file_size", "ext", "policy"}
    sortable_fields = {"id", "create_at", "update_at", "file_name", "file_size", "ext"}

    async def find_owned(
        self,
        file_info_id: str,
        user_id: str,
        *,
        for_update: bool = False,
    ) -> Optional[FileInfo]:
        query = select(self.model).where(
            self.model.id == file_info_id,
            self.model.user_id == user_id,
        )
        if for_update:
            query = query.with_for_update()
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def find_by_user_content(
        self,
        user_id: str,
        file_id: str,
        file_size: int,
    ) -> Optional[FileInfo]:
        query = select(self.model).where(
            self.model.user_id == user_id,
            self.model.file_id == file_id,
            self.model.file_size == file_size,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def count_content_references(self, file_id: str, file_size: int) -> int:
        query = select(func.count()).select_from(self.model).where(
            self.model.file_id == file_id,
            self.model.file_size == file_size,
        )
        return (await self.db.execute(query)).scalar() or 0

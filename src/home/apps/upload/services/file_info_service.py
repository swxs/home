# -*- coding: utf-8 -*-
# @File    : services/file_info_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict, Optional

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from home.web.schemas.types import objectId
from home.web.dependencies.session import get_session, transaction

from home.commons.Helpers import oss2_helper
from home.web.exceptions import Http403ForbiddenException
from home.web.schemas.pagination import PageSchema

# 本模块方法
from ..repositories.file_info_repository import FileInfoRepository
from ..repositories.file_share_link_repository import FileShareLinkRepository
from ..schemas.file_info import (
    FileInfoFilter,
    FileInfoOut,
    FileInfoUpdate,
)
from ..storage import build_object_key

logger = logging.getLogger("main.apps.upload.services.file_info_service")


class FileInfoService:
    """文件信息业务层：CRUD 编排与事务边界。"""

    def __init__(
        self,
        session: AsyncSession,
        repo: Optional[FileInfoRepository] = None,
        share_repo: Optional[FileShareLinkRepository] = None,
        oss_helper=None,
    ):
        self.session = session
        self.repo = repo or FileInfoRepository(session)
        self.share_repo = share_repo or FileShareLinkRepository(session)
        self.oss = oss_helper or oss2_helper

    @staticmethod
    def _forbidden() -> Http403ForbiddenException:
        return Http403ForbiddenException(
            Http403ForbiddenException.PasswordError,
            "无权访问该文件",
        )

    async def list(
        self,
        user_id: objectId,
        filter_schema: FileInfoFilter,
        page_schema: PageSchema,
    ) -> Dict[str, Any]:
        filter_schema.user_id = user_id
        result = await self.repo.search(filter_schema, page_schema)

        return {
            "data": [FileInfoOut.model_validate(fi) for fi in result["data"]],
            "pagination": result["pagination"],
        }

    async def get(self, user_id: objectId, file_info_id: objectId) -> FileInfoOut:
        file_info = await self.repo.find_owned(file_info_id, user_id)

        if file_info is None:
            raise self._forbidden()

        return FileInfoOut.model_validate(file_info)

    async def update(
        self,
        user_id: objectId,
        file_info_id: objectId,
        schema: FileInfoUpdate,
    ) -> FileInfoOut:
        file_info = await self.repo.find_owned(file_info_id, user_id)
        if file_info is None:
            raise self._forbidden()
        async with transaction(self.session):
            file_info = await self.repo.update_one(file_info_id, schema)

        return FileInfoOut.model_validate(file_info)

    async def delete(self, user_id: objectId, file_info_id: objectId) -> int:
        object_key = None
        async with transaction(self.session):
            file_info = await self.repo.find_owned(file_info_id, user_id, for_update=True)
            if file_info is None:
                raise self._forbidden()
            await self.share_repo.revoke_active_for_file(file_info_id)
            count = await self.repo.delete_one(file_info_id)
            references = await self.repo.count_content_references(
                file_info.file_id,
                file_info.file_size,
            )
            if references == 0:
                object_key = build_object_key(file_info.file_id, file_info.file_size)

        if object_key is not None:
            self.oss.delete(object_key)
        return count


async def get_file_info_service(session: AsyncSession = Depends(get_session)) -> FileInfoService:
    return FileInfoService(session)

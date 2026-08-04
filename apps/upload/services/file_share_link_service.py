# -*- coding: utf-8 -*-
# @File    : services/file_share_link_service.py
# @AUTH    : code_creater

import logging
import secrets
from datetime import datetime
from typing import Any, Dict, Optional, Tuple

from fastapi import Request
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db
from web.dependencies.transaction import transaction
from web.exceptions import Http400BadRequestException
from web.exceptions.http_403_forbidden_exception import Http403ForbiddenException
from web.schemas.pagination import PageSchema

# 本模块方法
from .. import consts
from ..repositories.file_info_repository import FileInfoRepository
from ..repositories.file_share_link_repository import FileShareLinkRepository
from ..schemas.file_share_link import (
    FileShareLinkCreate,
    FileShareLinkFilter,
    FileShareLinkOut,
    FileShareLinkPersist,
    FileShareLinkUpdate,
)
from .upload_service import UploadService

logger = logging.getLogger("main.apps.upload.services.file_share_link_service")


class FileShareLinkService:
    """文件分享链接业务层：创建、归属校验、公开访问与失效管理。"""

    def __init__(
        self,
        db: AsyncSession,
        repo: Optional[FileShareLinkRepository] = None,
        file_info_repo: Optional[FileInfoRepository] = None,
        upload_service: Optional[UploadService] = None,
    ):
        self.db = db
        self.repo = repo or FileShareLinkRepository(db)
        self.file_info_repo = file_info_repo or FileInfoRepository(db)
        self.upload_service = upload_service or UploadService(db, self.file_info_repo)

    @staticmethod
    def _generate_token() -> str:
        return secrets.token_urlsafe(32)

    @staticmethod
    def build_share_url(request: Request, token: str) -> str:
        base = str(request.base_url).rstrip("/")
        return f"{base}/api/upload/share/{token}"

    @staticmethod
    def _assert_owner(link, user_id: str) -> None:
        if link is None or str(link.create_by) != user_id:
            raise Http403ForbiddenException(
                Http403ForbiddenException.PasswordError,
                "无权操作该链接",
            )

    @staticmethod
    def _assert_active(link) -> None:
        if link.status != consts.ShareLinkStatus.ACTIVE:
            raise Http403ForbiddenException(
                Http403ForbiddenException.PasswordError,
                "链接已失效",
            )
        if link.expires_at is not None and link.expires_at <= datetime.now():
            raise Http403ForbiddenException(
                Http403ForbiddenException.PasswordError,
                "链接已过期",
            )

    async def _to_out(self, link, request: Optional[Request] = None) -> FileShareLinkOut:
        file_info = await self.file_info_repo.find_one(str(link.file_info_id))
        out = FileShareLinkOut.model_validate(link)
        out.file_name = file_info.file_name if file_info else None
        if request is not None:
            out.url = self.build_share_url(request, link.token)
        return out

    async def list_my(
        self,
        user_id: str,
        filter_schema: FileShareLinkFilter,
        page_schema: PageSchema,
        request: Request,
    ) -> Dict[str, Any]:
        filter_schema.create_by = user_id
        result = await self.repo.search(filter_schema, page_schema)

        return {
            "data": [await self._to_out(link, request) for link in result["data"]],
            "pagination": result["pagination"],
        }

    async def get_my(self, user_id: str, link_id: str, request: Request) -> FileShareLinkOut:
        link = await self.repo.find_one(link_id)
        self._assert_owner(link, user_id)
        return await self._to_out(link, request)

    async def create(
        self,
        user_id: str,
        schema: FileShareLinkCreate,
        request: Request,
    ) -> FileShareLinkOut:
        file_info = await self.file_info_repo.find_one(schema.file_info_id)
        if file_info is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "文件不存在")

        payload = FileShareLinkPersist(
            **schema.model_dump(),
            token=self._generate_token(),
            create_by=user_id,
            status=consts.ShareLinkStatus.ACTIVE,
        )

        async with transaction(self.db):
            link = await self.repo.create_one(payload)

        return await self._to_out(link, request)

    async def revoke(self, user_id: str, link_id: str, request: Request) -> FileShareLinkOut:
        link = await self.repo.find_one(link_id)
        self._assert_owner(link, user_id)

        async with transaction(self.db):
            link = await self.repo.update_one(
                link_id,
                FileShareLinkUpdate(status=consts.ShareLinkStatus.REVOKED),
            )

        return await self._to_out(link, request)

    async def delete(self, user_id: str, link_id: str) -> int:
        link = await self.repo.find_one(link_id)
        self._assert_owner(link, user_id)

        async with transaction(self.db):
            count = await self.repo.delete_one(link_id)

        return count

    async def access_by_token(self, token: str) -> Tuple[bytes, str, str, str]:
        link = await self.repo.find_by_token(token)
        if link is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "链接不存在")

        self._assert_active(link)
        return await self.upload_service.access(str(link.file_info_id))


async def get_file_share_link_service(
    db: AsyncSession = Depends(get_db),
) -> FileShareLinkService:
    return FileShareLinkService(db)

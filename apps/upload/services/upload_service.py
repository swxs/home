# -*- coding: utf-8 -*-
# @File    : services/upload_service.py
# @AUTH    : code_creater

import hashlib
import logging
import mimetypes
import os
from typing import Optional, Tuple

from fastapi import UploadFile
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.exceptions import Http400BadRequestException

# 通用方法
from commons.Helpers import oss2_helper
from web.dependencies.db import get_db
from web.dependencies.transaction import transaction
from web.exceptions import Http403ForbiddenException

# 本模块方法
from .. import consts
from ..repositories.file_info_repository import FileInfoRepository
from ..schemas.file_info import FileInfoOut, FileInfoPersist
from ..storage import build_object_key
from .file_info_service import FileInfoService

logger = logging.getLogger("main.apps.upload.services.upload_service")


class UploadService:
    """文件上传/下载业务层：封装 OSS 存储与文件记录的联动及事务边界。"""

    def __init__(self, db: AsyncSession, repo: Optional[FileInfoRepository] = None):
        self.db = db
        self.repo = repo or FileInfoRepository(db)

    @staticmethod
    def _normalize_ext(ext: Optional[str]) -> str:
        if not ext:
            return ""
        normalized = ext.lower()
        return normalized if normalized.startswith(".") else f".{normalized}"

    @classmethod
    def is_image(cls, ext: Optional[str]) -> bool:
        return cls._normalize_ext(ext) in consts.IMAGE_EXTENSIONS

    @staticmethod
    def guess_media_type(filename: str) -> str:
        media_type, _ = mimetypes.guess_type(filename)
        return media_type or "application/octet-stream"

    @classmethod
    def resolve_access_mode(cls, ext: Optional[str], mode: Optional[str] = None) -> consts.AccessMode:
        if mode is not None:
            try:
                return consts.AccessMode(mode)
            except ValueError as exc:
                raise Http400BadRequestException(
                    Http400BadRequestException.IllegalArgument,
                    "mode 仅支持 inline 或 download",
                ) from exc

        if cls.is_image(ext):
            return consts.AccessMode.INLINE
        return consts.AccessMode.DOWNLOAD

    async def upload_file(self, user_id: str, file: UploadFile) -> FileInfoOut:
        """兼容旧中转上传端点；新客户端应使用 Presigned 直传。"""
        data = await file.read()
        file_id = hashlib.md5(data).hexdigest()
        filename = file.filename if file.filename else "unknown"
        file_size = len(data)
        existing = await self.repo.find_by_user_content(user_id, file_id, file_size)
        if existing is not None:
            return FileInfoOut.model_validate(existing)

        object_key = build_object_key(file_id, file_size)
        if not oss2_helper.exists(object_key):
            oss2_helper.upload(
                object_key,
                data,
                content_type=self.guess_media_type(filename),
            )

        file_info_schema = FileInfoPersist(
            user_id=user_id,
            file_id=file_id,
            file_name=filename,
            file_size=file_size,
            ext=os.path.splitext(filename)[1],
            policy=consts.FileInfo_Policy.ALIOSS,
        )
        async with transaction(self.db):
            file_info = await self.repo.create_one(file_info_schema)

        return FileInfoOut.model_validate(file_info)

    async def _find_owned(self, user_id: str, file_info_id: str):
        file_info = await self.repo.find_owned(file_info_id, user_id)
        if file_info is None:
            raise Http403ForbiddenException(
                Http403ForbiddenException.PasswordError,
                "无权访问该文件",
            )
        return file_info

    async def download(self, user_id: str, file_info_id: str) -> Tuple[bytes, str]:
        file_info = await self._find_owned(user_id, file_info_id)
        data = oss2_helper.download(build_object_key(file_info.file_id, file_info.file_size))
        return data, file_info.file_name

    async def access(
        self,
        file_info_id: str,
        mode: Optional[str] = None,
    ) -> Tuple[bytes, str, str, str]:
        file_info = await self.repo.find_one(file_info_id)
        access_mode = self.resolve_access_mode(file_info.ext, mode)
        data = oss2_helper.download(build_object_key(file_info.file_id, file_info.file_size))
        media_type = self.guess_media_type(file_info.file_name)
        disposition = "inline" if access_mode == consts.AccessMode.INLINE else "attachment"
        return data, file_info.file_name, media_type, disposition

    async def delete(self, user_id: str, file_info_id: str) -> int:
        service = FileInfoService(self.db, repo=self.repo, oss_helper=oss2_helper)
        return await service.delete(user_id, file_info_id)

    async def signed_path(self, user_id: str, file_info_id: str) -> str:
        file_info = await self._find_owned(user_id, file_info_id)

        return oss2_helper.get_sign_download_path(
            build_object_key(file_info.file_id, file_info.file_size),
            file_info.file_name,
        )


async def get_upload_service(db: AsyncSession = Depends(get_db)) -> UploadService:
    return UploadService(db)

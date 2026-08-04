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

# 本模块方法
from .. import consts
from ..repositories.file_info_repository import FileInfoRepository
from ..schemas.file_info import FileInfoCreate, FileInfoOut

logger = logging.getLogger("main.apps.upload.services.upload_service")


class UploadService:
    """文件上传/下载业务层：封装 OSS 存储与文件记录的联动及事务边界。"""

    def __init__(self, db: AsyncSession, repo: Optional[FileInfoRepository] = None):
        self.db = db
        self.repo = repo or FileInfoRepository(db)

    @staticmethod
    def _object_key(file_id: str) -> str:
        return f"{file_id[:4]}/{file_id[4:]}"

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

    async def upload_file(self, file: UploadFile) -> FileInfoOut:
        data = await file.read()
        file_id = hashlib.md5(data).hexdigest()
        filename = file.filename if file.filename else "unknown"

        oss2_helper.upload(self._object_key(file_id), data)

        file_info_schema = FileInfoCreate(
            file_id=file_id,
            file_name=filename,
            file_size=file.size,
            ext=os.path.splitext(filename)[1],
            policy=consts.FileInfo_Policy.ALIOSS,
        )
        async with transaction(self.db):
            file_info = await self.repo.create_one(file_info_schema)

        return FileInfoOut.model_validate(file_info)

    async def download(self, file_info_id: str) -> Tuple[bytes, str]:
        file_info = await self.repo.find_one(file_info_id)

        data = oss2_helper.download(self._object_key(file_info.file_id))
        return data, file_info.file_name

    async def access(
        self,
        file_info_id: str,
        mode: Optional[str] = None,
    ) -> Tuple[bytes, str, str, str]:
        file_info = await self.repo.find_one(file_info_id)
        access_mode = self.resolve_access_mode(file_info.ext, mode)
        data = oss2_helper.download(self._object_key(file_info.file_id))
        media_type = self.guess_media_type(file_info.file_name)
        disposition = "inline" if access_mode == consts.AccessMode.INLINE else "attachment"
        return data, file_info.file_name, media_type, disposition

    async def delete(self, file_info_id: str) -> int:
        async with transaction(self.db):
            file_info = await self.repo.find_one(file_info_id)
            oss2_helper.delete(self._object_key(file_info.file_id))
            count = await self.repo.delete_one(file_info_id)

        return count

    async def signed_path(self, file_info_id: str) -> str:
        file_info = await self.repo.find_one(file_info_id)

        return oss2_helper.get_sign_download_path(
            self._object_key(file_info.file_id),
            file_info.file_name,
        )


async def get_upload_service(db: AsyncSession = Depends(get_db)) -> UploadService:
    return UploadService(db)

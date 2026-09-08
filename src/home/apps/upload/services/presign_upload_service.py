"""Presigned OSS 上传、确认与下载业务。"""

import os
from typing import Optional

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from home.commons.Helpers import oss2_helper
from home.core import config
from home.web.dependencies.db import get_db
from home.web.dependencies.transaction import transaction
from home.web.exceptions import Http400BadRequestException

# 本模块方法
from .. import consts
from ..repositories.file_info_repository import FileInfoRepository
from ..schemas.file_info import FileInfoOut, FileInfoPersist
from ..schemas.presign import (
    PresignCompleteRequest,
    PresignDownloadOut,
    PresignUploadOut,
    PresignUploadRequest,
)
from ..storage import build_object_key
from .file_info_service import FileInfoService


class PresignUploadService:
    def __init__(
        self,
        db: AsyncSession,
        repo: Optional[FileInfoRepository] = None,
        oss_helper=None,
        *,
        upload_max_bytes: int = config.UPLOAD_MAX_BYTES,
        upload_expires: int = config.UPLOAD_PRESIGN_EXPIRES,
        download_expires: int = config.DOWNLOAD_PRESIGN_EXPIRES,
    ):
        self.db = db
        self.repo = repo or FileInfoRepository(db)
        self.oss = oss_helper or oss2_helper
        self.upload_max_bytes = upload_max_bytes
        self.upload_expires = upload_expires
        self.download_expires = download_expires

    def _validate_size(self, file_size: int) -> None:
        if file_size > self.upload_max_bytes:
            raise Http400BadRequestException(
                Http400BadRequestException.IllegalArgument,
                f"文件不能超过 {self.upload_max_bytes} 字节",
            )

    @staticmethod
    def _validate_object_meta(
        expected_size: int,
        expected_content_type: str,
        actual_size: int,
        actual_content_type: Optional[str],
    ) -> None:
        if actual_size != expected_size:
            raise Http400BadRequestException(
                Http400BadRequestException.IllegalArgument,
                "OSS 对象大小与申请信息不一致",
            )
        if actual_content_type != expected_content_type:
            raise Http400BadRequestException(
                Http400BadRequestException.IllegalArgument,
                "OSS 对象 Content-Type 与申请信息不一致",
            )

    async def _create_or_get(
        self,
        user_id: str,
        schema: PresignCompleteRequest | PresignUploadRequest,
    ) -> FileInfoOut:
        existing = await self.repo.find_by_user_content(
            user_id,
            schema.file_id,
            schema.file_size,
        )
        if existing is not None:
            return FileInfoOut.model_validate(existing)

        payload = FileInfoPersist(
            user_id=user_id,
            file_id=schema.file_id,
            file_name=schema.file_name,
            file_size=schema.file_size,
            ext=os.path.splitext(schema.file_name)[1].lower(),
            policy=consts.FileInfo_Policy.ALIOSS,
        )
        try:
            async with transaction(self.db):
                file_info = await self.repo.create_one(payload)
        except Http400BadRequestException:
            # 组合唯一约束负责消化并发 complete；事务回滚后读取胜出记录。
            existing = await self.repo.find_by_user_content(
                user_id,
                schema.file_id,
                schema.file_size,
            )
            if existing is None:
                raise
            file_info = existing
        return FileInfoOut.model_validate(file_info)

    async def presign_upload(
        self,
        user_id: str,
        schema: PresignUploadRequest,
    ) -> PresignUploadOut:
        self._validate_size(schema.file_size)
        key = build_object_key(schema.file_id, schema.file_size)
        if self.oss.exists(key):
            _, content_type, content_length = self.oss.get_file_meta(key)
            self._validate_object_meta(
                schema.file_size,
                schema.content_type,
                content_length,
                content_type,
            )
            file_info = await self._create_or_get(user_id, schema)
            return PresignUploadOut(
                skip_upload=True,
                expires_in=self.upload_expires,
                file_id=schema.file_id,
                data=file_info,
            )

        return PresignUploadOut(
            skip_upload=False,
            presigned_url=self.oss.sign_put_url(
                key,
                schema.content_type,
                schema.content_md5,
                self.upload_expires,
            ),
            expires_in=self.upload_expires,
            file_id=schema.file_id,
        )

    async def complete(
        self,
        user_id: str,
        schema: PresignCompleteRequest,
    ) -> FileInfoOut:
        self._validate_size(schema.file_size)
        key = build_object_key(schema.file_id, schema.file_size)
        if not self.oss.exists(key):
            raise Http400BadRequestException(
                Http400BadRequestException.NoResource,
                "OSS 对象不存在，请先完成上传",
            )
        _, content_type, content_length = self.oss.get_file_meta(key)
        self._validate_object_meta(
            schema.file_size,
            schema.content_type,
            content_length,
            content_type,
        )
        return await self._create_or_get(user_id, schema)

    async def download(
        self,
        user_id: str,
        file_info_id: str,
        disposition: str,
    ) -> PresignDownloadOut:
        file_info_service = FileInfoService(
            self.db,
            repo=self.repo,
            oss_helper=self.oss,
        )
        file_info = await file_info_service.get(user_id, file_info_id)
        url = self.oss.sign_get_url(
            build_object_key(file_info.file_id, file_info.file_size),
            file_info.file_name,
            disposition,
            self.download_expires,
        )
        return PresignDownloadOut(url=url, expires_in=self.download_expires)


async def get_presign_upload_service(
    db: AsyncSession = Depends(get_db),
) -> PresignUploadService:
    return PresignUploadService(db)

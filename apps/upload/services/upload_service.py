# -*- coding: utf-8 -*-
# @File    : services/upload_service.py
# @AUTH    : code_creater

import os
import hashlib
import logging
from typing import Tuple

from fastapi import UploadFile
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# 通用方法
from commons.Helpers import oss2_helper
from web.dependencies.db import get_db, get_single_worker

# 本模块方法
from .. import consts
from ..models.file_info import FileInfo
from ..schemas.file_info import FileInfoCreate, FileInfoOut

logger = logging.getLogger("main.apps.upload.services.upload_service")


class UploadService:
    """文件上传/下载业务层：封装 OSS 存储与文件记录的联动及事务边界。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    @staticmethod
    def _object_key(file_id: str) -> str:
        return f"{file_id[:4]}/{file_id[4:]}"

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
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            file_info = await worker.repository.create_one(file_info_schema)

        return FileInfoOut.model_validate(file_info)

    async def download(self, file_info_id: str) -> Tuple[bytes, str]:
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            file_info = await worker.repository.find_one(file_info_id)

        data = oss2_helper.download(self._object_key(file_info.file_id))
        return data, file_info.file_name

    async def delete(self, file_info_id: str) -> int:
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            file_info = await worker.repository.find_one(file_info_id)
            oss2_helper.delete(self._object_key(file_info.file_id))
            count = await worker.repository.delete_one(file_info_id)

        return count

    async def signed_path(self, file_info_id: str) -> str:
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            file_info = await worker.repository.find_one(file_info_id)

        return oss2_helper.get_sign_download_path(
            self._object_key(file_info.file_id),
            file_info.file_name,
        )


async def get_upload_service(db: AsyncSession = Depends(get_db)) -> UploadService:
    return UploadService(db)

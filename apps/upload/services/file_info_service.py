# -*- coding: utf-8 -*-
# @File    : services/file_info_service.py
# @AUTH    : code_creater

import logging
from typing import Any, Dict

from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.schemas.pagination import PageSchema

# 本模块方法
from ..models.file_info import FileInfo
from ..schemas.file_info import (
    FileInfoCreate,
    FileInfoFilter,
    FileInfoOut,
    FileInfoUpdate,
)

logger = logging.getLogger("main.apps.upload.services.file_info_service")


class FileInfoService:
    """文件信息业务层：CRUD 编排与事务边界。"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list(self, filter_schema: FileInfoFilter, page_schema: PageSchema) -> Dict[str, Any]:
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            result = await worker.repository.search(filter_schema, page_schema)

        return {
            "data": [FileInfoOut.model_validate(fi) for fi in result["data"]],
            "pagination": result["pagination"],
        }

    async def get(self, file_info_id: str) -> FileInfoOut:
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            file_info = await worker.repository.find_one(file_info_id)

        if file_info is None:
            raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

        return FileInfoOut.model_validate(file_info)

    async def create(self, schema: FileInfoCreate) -> FileInfoOut:
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            file_info = await worker.repository.create_one(schema)

        return FileInfoOut.model_validate(file_info)

    async def update(self, file_info_id: str, schema: FileInfoUpdate) -> FileInfoOut:
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            file_info = await worker.repository.update_one(file_info_id, schema)

        return FileInfoOut.model_validate(file_info)

    async def delete(self, file_info_id: str) -> int:
        single_worker = await get_single_worker(self.db, FileInfo)
        async with single_worker as worker:
            count = await worker.repository.delete_one(file_info_id)

        return count


async def get_file_info_service(db: AsyncSession = Depends(get_db)) -> FileInfoService:
    return FileInfoService(db)

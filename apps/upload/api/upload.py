# -*- coding: utf-8 -*-
# @File    : api/upload.py
# @AUTH    : code_creater

import io
import os
import hashlib
import logging
from typing import Any

from fastapi import APIRouter, Body, Path, Query, UploadFile
from fastapi.param_functions import Depends
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.search import SearchSchema, get_search
from web.dependencies.token import TokenSchema, get_token
from web.exceptions import Http400BadRequestException
from web.response import CustomFileresponse, success

# 通用方法
from commons.Helpers import oss2_helper

# 本模块方法
from .. import consts, file_info_utils
from ..repositories.file_info_repository import FileInfoRepository
from ..schemas.file_info import FileInfoSchema

router = APIRouter()

logger = logging.getLogger("main.apps.upload")


@router.post("/")
async def upload_file(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
):
    data = await file.read()
    file_id = hashlib.md5(data).hexdigest()
    filename = file.filename if file.filename else "unknown"
    try:
        oss2_helper.upload(f"{file_id[:4]}/{file_id[4:]}", data)
    except Exception as e:
        raise e

    file_info_repo = FileInfoRepository(db)
    file_info_schema = FileInfoSchema(
        file_id=file_id,
        file_name=filename,
        file_size=file.size,
        ext=os.path.splitext(filename)[1],
        policy=consts.FileInfo_Policy.ALIOSS,
    )
    file_info = await file_info_repo.create_one(file_info_schema, "文件信息创建失败")

    file_info_response = FileInfoSchema.model_validate(file_info)
    return success(data=file_info_response.model_dump())


@router.get("/{file_info_id}")
async def download_file(
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    file_info_repo = FileInfoRepository(db)
    file_info = await file_info_repo.find_one(file_info_id, "文件信息不存在")

    return CustomFileresponse(
        data=oss2_helper.download(f"{file_info.file_id[:4]}/{file_info.file_id[4:]}"),
        filename=file_info.file_name,
    )


@router.delete("/{file_info_id}")
async def delete_file(
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    file_info_repo = FileInfoRepository(db)
    file_info = await file_info_repo.find_one(file_info_id, "文件信息不存在")

    oss2_helper.delete(f"{file_info.file_id[:4]}/{file_info.file_id[4:]}")
    count = await file_info_repo.delete_one(file_info_id, "文件信息不存在", "文件删除失败")

    return success(
        {
            "count": count,
        }
    )


@router.get("/path/{file_info_id}")
async def path(
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    file_info_repo = FileInfoRepository(db)
    file_info = await file_info_repo.find_one(file_info_id, "文件信息不存在")

    return success(
        data={
            "path": oss2_helper.get_sign_download_path(
                f"{file_info.file_id[:4]}/{file_info.file_id[4:]}",
                file_info.file_name,
            ),
        },
    )

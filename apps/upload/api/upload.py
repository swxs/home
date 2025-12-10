# -*- coding: utf-8 -*-
# @File    : api/upload.py
# @AUTH    : code_creater

import os
import hashlib
import logging

from fastapi import APIRouter, Body, Path, Query, UploadFile
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.response import CustomFileresponse, success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 通用方法
from commons.Helpers import oss2_helper

# 本模块方法
from .. import consts
from ..models.file_info import FileInfo
from ..schemas.file_info import FileInfoSchema
from ..schemas.response import CountResponse, FileInfoResponse, FilePathResponse

router = APIRouter()

logger = logging.getLogger("main.apps.upload.api.upload")


@router.post("/", response_model=SuccessResponse[FileInfoResponse])
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

    file_info_schema = FileInfoSchema(
        file_id=file_id,
        file_name=filename,
        file_size=file.size,
        ext=os.path.splitext(filename)[1],
        policy=consts.FileInfo_Policy.ALIOSS,
    )
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        file_info = await worker.repository.create_one(file_info_schema)

    file_info_response = FileInfoSchema.model_validate(file_info)
    return success(
        {
            "data": file_info_response.model_dump(),
        }
    )


@router.get("/{file_info_id}")
async def download_file(
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
) -> CustomFileresponse:
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        file_info = await worker.repository.find_one(file_info_id)

    return CustomFileresponse(
        data=oss2_helper.download(f"{file_info.file_id[:4]}/{file_info.file_id[4:]}"),
        filename=file_info.file_name,
    )


@router.delete("/{file_info_id}", response_model=SuccessResponse[CountResponse])
async def delete_file(
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        file_info = await worker.repository.find_one(file_info_id)
        oss2_helper.delete(f"{file_info.file_id[:4]}/{file_info.file_id[4:]}")
        count = await worker.repository.delete_one(file_info_id)

    return success(
        {
            "count": count,
        }
    )


@router.get("/path/{file_info_id}", response_model=SuccessResponse[FilePathResponse])
async def path(
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        file_info = await worker.repository.find_one(file_info_id)

    return success(
        {
            "path": oss2_helper.get_sign_download_path(
                f"{file_info.file_id[:4]}/{file_info.file_id[4:]}",
                file_info.file_name,
            ),
        }
    )

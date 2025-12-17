# -*- coding: utf-8 -*-
# @File    : api/file_info.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import CountResponse, SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..models.file_info import FileInfo
from ..schemas.file_info import FileInfoSchema, get_file_info_schema
from ..schemas.response import FileInfoResponse, FileInfoSearchResponse

router = APIRouter()

logger = logging.getLogger("main.apps.upload.api.file_info")


@router.get("/", response_model=SuccessResponse[FileInfoSearchResponse])
async def get_file_info_list(
    token_schema: TokenSchema = Depends(get_token),
    file_info_schema: FileInfoSchema = Depends(get_file_info_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        result = await worker.repository.search(file_info_schema, page_schema)

    return success(
        {
            "data": [FileInfoSchema.model_validate(fi) for fi in result["data"]],
            "pagination": result["pagination"],
        }
    )


@router.get("/{file_info_id}", response_model=SuccessResponse[FileInfoResponse])
async def get_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        file_info = await worker.repository.find_one(file_info_id)

    if file_info is None:
        raise Http400BadRequestException(Http400BadRequestException.NoResource, "数据不存在")

    return success(
        {
            "data": FileInfoSchema.model_validate(file_info),
        }
    )


@router.post("/", response_model=SuccessResponse[FileInfoResponse])
async def create_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_schema: FileInfoSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        file_info = await worker.repository.create_one(file_info_schema)

    return success(
        {
            "data": FileInfoSchema.model_validate(file_info),
        }
    )


@router.put("/{file_info_id}", response_model=SuccessResponse[FileInfoResponse])
async def modify_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    file_info_schema: FileInfoSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        file_info = await worker.repository.update_one(file_info_id, file_info_schema)

    return success(
        {
            "data": FileInfoSchema.model_validate(file_info),
        }
    )


@router.delete("/{file_info_id}", response_model=SuccessResponse[CountResponse])
async def delete_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    single_worker = await get_single_worker(db, FileInfo)
    async with single_worker as worker:
        count = await worker.repository.delete_one(file_info_id)

    return success(
        {
            "count": count,
        }
    )

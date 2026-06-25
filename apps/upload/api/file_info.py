# -*- coding: utf-8 -*-
# @File    : api/file_info.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path
from fastapi.param_functions import Depends

from web.response import success
from web.schemas.pagination import PageSchema, get_pagination
from web.schemas.response import CountResponse, SuccessResponse
from web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.file_info import (
    FileInfoCreate,
    FileInfoFilter,
    FileInfoUpdate,
    get_file_info_filter,
)
from ..schemas.response import FileInfoResponse, FileInfoSearchResponse
from ..services.file_info_service import FileInfoService, get_file_info_service

router = APIRouter()

logger = logging.getLogger("main.apps.upload.api.file_info")


@router.get("/", response_model=SuccessResponse[FileInfoSearchResponse])
async def get_file_info_list(
    token_schema: TokenSchema = Depends(get_token),
    filter_schema: FileInfoFilter = Depends(get_file_info_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: FileInfoService = Depends(get_file_info_service),
):
    result = await service.list(filter_schema, page_schema)
    return success(result)


@router.get("/{file_info_id}", response_model=SuccessResponse[FileInfoResponse])
async def get_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: FileInfoService = Depends(get_file_info_service),
):
    file_info = await service.get(file_info_id)
    return success({"data": file_info})


@router.post("/", response_model=SuccessResponse[FileInfoResponse])
async def create_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_schema: FileInfoCreate = Body(...),
    service: FileInfoService = Depends(get_file_info_service),
):
    file_info = await service.create(file_info_schema)
    return success({"data": file_info})


@router.put("/{file_info_id}", response_model=SuccessResponse[FileInfoResponse])
async def modify_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    file_info_schema: FileInfoUpdate = Body(...),
    service: FileInfoService = Depends(get_file_info_service),
):
    file_info = await service.update(file_info_id, file_info_schema)
    return success({"data": file_info})


@router.delete("/{file_info_id}", response_model=SuccessResponse[CountResponse])
async def delete_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: FileInfoService = Depends(get_file_info_service),
):
    count = await service.delete(file_info_id)
    return success({"count": count})

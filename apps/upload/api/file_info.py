# -*- coding: utf-8 -*-
# @File    : api/file_info.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.token import TokenSchema, get_token
from web.exceptions import Http400BadRequestException
from web.response import success

# 本模块方法
from ..repositories.file_info_repository import FileInfoRepository
from ..schemas.file_info import FileInfoSchema, get_file_info_schema

router = APIRouter()

logger = logging.getLogger("main.apps.upload.api.file_info")


@router.get("/")
async def get_file_info_list(
    token_schema: TokenSchema = Depends(get_token),
    file_info_schema: FileInfoSchema = Depends(get_file_info_schema),
    page_schema: PageSchema = Depends(get_pagination),
    db: AsyncSession = Depends(get_db),
):
    file_info_repo = FileInfoRepository(db)

    # 使用Repository搜索方法
    result = await file_info_repo.search(file_info_schema, page_schema)

    # 转换为 Schema
    file_info_list = [FileInfoSchema.model_validate(fi).model_dump() for fi in result["data"]]

    return success(
        {
            "data": file_info_list,
            "pagination": result["pagination"].model_dump(),
        }
    )


@router.get("/{file_info_id}")
async def get_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    file_info_repo = FileInfoRepository(db)

    # 使用Repository查找方法
    file_info = await file_info_repo.find_one(file_info_id, "文件信息不存在")

    # 转换为 Schema
    file_info_response = FileInfoSchema.model_validate(file_info)

    return success(
        {
            "data": file_info_response.model_dump(),
        }
    )


@router.post("/")
async def create_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_schema: FileInfoSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    file_info_repo = FileInfoRepository(db)

    # 使用Repository创建方法
    file_info = await file_info_repo.create_one(file_info_schema, "文件信息创建失败")

    file_info_response = FileInfoSchema.model_validate(file_info)

    return success(
        {
            "data": file_info_response.model_dump(),
        }
    )


@router.put("/{file_info_id}")
async def modify_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    file_info_schema: FileInfoSchema = Body(...),
    db: AsyncSession = Depends(get_db),
):
    file_info_repo = FileInfoRepository(db)

    # 使用Repository更新方法
    file_info = await file_info_repo.update_one(
        file_info_id,
        file_info_schema,
        "文件信息不存在",
        "文件信息更新失败",
    )

    # 转换为 Schema
    file_info_response = FileInfoSchema.model_validate(file_info)

    return success(
        {
            "data": file_info_response.model_dump(),
        }
    )


@router.delete("/{file_info_id}")
async def delete_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    db: AsyncSession = Depends(get_db),
):
    file_info_repo = FileInfoRepository(db)

    # 使用Repository删除方法
    count = await file_info_repo.delete_one(file_info_id, "文件信息不存在", "文件信息删除失败")

    return success(
        {
            "count": count,
        }
    )

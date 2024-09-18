# -*- coding: utf-8 -*-
# @File    : api/file_info.py
# @AUTH    : code_creater

import logging

from bson import ObjectId
from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends

from web.custom_types import OID
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.token import TokenSchema, get_token
from web.response import success

# 本模块方法
from ..dao.file_info import FileInfo
from ..schemas.file_info import FileInfoSchema, get_file_info_schema

router = APIRouter()

logger = logging.getLogger("main.apps.upload.api.file_info")


@router.get("/")
async def get_file_info_list(
    token_schema: TokenSchema = Depends(get_token),
    file_info_schema: FileInfoSchema = Depends(get_file_info_schema),
    page_schema: PageSchema = Depends(get_pagination),
):
    file_info_list = (
        await FileInfo.search(
            searches=file_info_schema.dict(exclude_unset=True),
            skip=page_schema.skip,
            limit=page_schema.limit,
        )
    ).order_by(page_schema.order_by)

    pagination = PaginationSchema(
        total=await FileInfo.count(
            finds=file_info_schema.dict(exclude_unset=True),
        ),
        order_by=page_schema.order_by,
        use_pager=page_schema.use_pager,
        page=page_schema.page,
        page_number=page_schema.page_number,
    )

    return success(
        {
            "data": await file_info_list.to_dict(),
            "pagination": pagination.dict(),
        }
    )


@router.get("/{file_info_id}")
async def get_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    file_info = await FileInfo.find_one(
        finds={"id": ObjectId(file_info_id)},
        nullable=False,
    )

    return success(
        {
            "data": file_info,
        }
    )


@router.post("/")
async def create_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_schema: FileInfoSchema = Body(...),
):
    file_info = await FileInfo.create(
        params=file_info_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": file_info,
        }
    )


@router.put("/{file_info_id}")
async def modify_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: OID = Path(..., regex="[0-9a-f]{24}"),
    file_info_schema: FileInfoSchema = Body(...),
):
    file_info = await FileInfo.update_one(
        finds={"id": ObjectId(file_info_id)},
        params=file_info_schema.dict(exclude_defaults=True),
    )

    return success(
        {
            "data": file_info,
        }
    )


@router.delete("/{file_info_id}")
async def delete_file_info(
    token_schema: TokenSchema = Depends(get_token),
    file_info_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    count = await FileInfo.delete_one(
        finds={"id": ObjectId(file_info_id)},
    )

    return success(
        {
            "count": count,
        }
    )

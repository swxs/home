# -*- coding: utf-8 -*-
# @File    : api/file_share_link.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Body, Path, Request
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.pagination import PageSchema, get_pagination
from home.web.schemas.response import CountResponse, SuccessResponse
from home.web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.file_share_link import (
    FileShareLinkCreate,
    FileShareLinkFilter,
    get_file_share_link_filter,
)
from ..schemas.response import FileShareLinkResponse, FileShareLinkSearchResponse
from ..services.file_share_link_service import (
    FileShareLinkService,
    get_file_share_link_service,
)

router = APIRouter()

logger = logging.getLogger("main.apps.upload.api.file_share_link")


@router.get("/", response_model=SuccessResponse[FileShareLinkSearchResponse])
async def get_file_share_link_list(
    request: Request,
    token_schema: TokenSchema = Depends(get_token),
    filter_schema: FileShareLinkFilter = Depends(get_file_share_link_filter),
    page_schema: PageSchema = Depends(get_pagination),
    service: FileShareLinkService = Depends(get_file_share_link_service),
):
    result = await service.list_my(token_schema.user_id, filter_schema, page_schema, request)
    return success(result)


@router.get("/{link_id}", response_model=SuccessResponse[FileShareLinkResponse])
async def get_file_share_link(
    request: Request,
    token_schema: TokenSchema = Depends(get_token),
    link_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: FileShareLinkService = Depends(get_file_share_link_service),
):
    link = await service.get_my(token_schema.user_id, link_id, request)
    return success({"data": link})


@router.post("/", response_model=SuccessResponse[FileShareLinkResponse])
async def create_file_share_link(
    request: Request,
    token_schema: TokenSchema = Depends(get_token),
    schema: FileShareLinkCreate = Body(...),
    service: FileShareLinkService = Depends(get_file_share_link_service),
):
    link = await service.create(token_schema.user_id, schema, request)
    return success({"data": link})


@router.put("/{link_id}/revoke", response_model=SuccessResponse[FileShareLinkResponse])
async def revoke_file_share_link(
    request: Request,
    token_schema: TokenSchema = Depends(get_token),
    link_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: FileShareLinkService = Depends(get_file_share_link_service),
):
    link = await service.revoke(token_schema.user_id, link_id, request)
    return success({"data": link})


@router.delete("/{link_id}", response_model=SuccessResponse[CountResponse])
async def delete_file_share_link(
    token_schema: TokenSchema = Depends(get_token),
    link_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    service: FileShareLinkService = Depends(get_file_share_link_service),
):
    count = await service.delete(token_schema.user_id, link_id)
    return success({"count": count})

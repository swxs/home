# -*- coding: utf-8 -*-

from typing import Literal

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.response import SuccessResponse
from home.web.schemas.token import TokenSchema, get_token

# 本模块方法
from ..schemas.presign import (
    PresignCompleteRequest,
    PresignDownloadOut,
    PresignUploadOut,
    PresignUploadRequest,
)
from ..schemas.response import FileInfoResponse
from ..services.presign_upload_service import (
    PresignUploadService,
    get_presign_upload_service,
)

router = APIRouter()


@router.post("/upload", response_model=SuccessResponse[PresignUploadOut])
async def presign_upload(
    schema: PresignUploadRequest = Body(...),
    token_schema: TokenSchema = Depends(get_token),
    service: PresignUploadService = Depends(get_presign_upload_service),
):
    result = await service.presign_upload(token_schema.user_id, schema)
    return success(result)


@router.post("/complete", response_model=SuccessResponse[FileInfoResponse])
async def complete_upload(
    schema: PresignCompleteRequest = Body(...),
    token_schema: TokenSchema = Depends(get_token),
    service: PresignUploadService = Depends(get_presign_upload_service),
):
    file_info = await service.complete(token_schema.user_id, schema)
    return success({"data": file_info})


@router.get(
    "/download/{file_info_id}",
    response_model=SuccessResponse[PresignDownloadOut],
)
async def presign_download(
    file_info_id: str = Path(..., regex="[0-9a-fA-F]{24}"),
    disposition: Literal["inline", "attachment"] = Query("inline"),
    token_schema: TokenSchema = Depends(get_token),
    service: PresignUploadService = Depends(get_presign_upload_service),
):
    result = await service.download(
        token_schema.user_id,
        file_info_id,
        disposition,
    )
    return success(result)

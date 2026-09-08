# -*- coding: utf-8 -*-

from typing import Literal

from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.types import objectId
from home.web.schemas.response import SuccessResponse
from home.web.schemas.token import get_required_user_id

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
    user_id: objectId = Depends(get_required_user_id),
    service: PresignUploadService = Depends(get_presign_upload_service),
):
    result = await service.presign_upload(user_id, schema)
    return success(result)


@router.post("/complete", response_model=SuccessResponse[FileInfoResponse])
async def complete_upload(
    schema: PresignCompleteRequest = Body(...),
    user_id: objectId = Depends(get_required_user_id),
    service: PresignUploadService = Depends(get_presign_upload_service),
):
    file_info = await service.complete(user_id, schema)
    return success({"data": file_info})


@router.get(
    "/download/{file_info_id}",
    response_model=SuccessResponse[PresignDownloadOut],
)
async def presign_download(
    file_info_id: objectId = Path(...),
    disposition: Literal["inline", "attachment"] = Query("inline"),
    user_id: objectId = Depends(get_required_user_id),
    service: PresignUploadService = Depends(get_presign_upload_service),
):
    result = await service.download(
        user_id,
        file_info_id,
        disposition,
    )
    return success(result)

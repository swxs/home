from home.web.schemas.types import objectId
# -*- coding: utf-8 -*-
# @File    : api/upload.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Path, UploadFile
from fastapi.param_functions import Depends

from home.web.response import CustomFileresponse, success
from home.web.schemas.response import CountResponse, SuccessResponse
from home.web.schemas.token import get_required_user_id

# 本模块方法
from ..schemas.response import FileInfoResponse, FilePathResponse
from ..services.upload_service import UploadService, get_upload_service

router = APIRouter()

logger = logging.getLogger("main.apps.upload.api.upload")


@router.post(
    "/",
    response_model=SuccessResponse[FileInfoResponse],
    deprecated=True,
)
async def upload_file(
    file: UploadFile,
    user_id: objectId = Depends(get_required_user_id),
    service: UploadService = Depends(get_upload_service),
):
    file_info = await service.upload_file(user_id, file)
    return success({"data": file_info})


@router.get("/path/{file_info_id}", response_model=SuccessResponse[FilePathResponse], deprecated=True)
async def path(
    file_info_id: objectId = Path(...),
    user_id: objectId = Depends(get_required_user_id),
    service: UploadService = Depends(get_upload_service),
):
    signed = await service.signed_path(user_id, file_info_id)
    return success({"path": signed})


@router.get("/{file_info_id}")
async def download_file(
    file_info_id: objectId = Path(...),
    user_id: objectId = Depends(get_required_user_id),
    service: UploadService = Depends(get_upload_service),
) -> CustomFileresponse:
    data, filename = await service.download(user_id, file_info_id)
    return CustomFileresponse(data=data, filename=filename)


@router.delete(
    "/{file_info_id}",
    response_model=SuccessResponse[CountResponse],
    deprecated=True,
)
async def delete_file(
    file_info_id: objectId = Path(...),
    user_id: objectId = Depends(get_required_user_id),
    service: UploadService = Depends(get_upload_service),
):
    count = await service.delete(user_id, file_info_id)
    return success({"count": count})

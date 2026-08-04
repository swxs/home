# -*- coding: utf-8 -*-
# @File    : api/share.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, Path
from fastapi.param_functions import Depends

from web.response import CustomFileresponse

# 本模块方法
from ..services.file_share_link_service import (
    FileShareLinkService,
    get_file_share_link_service,
)

router = APIRouter()

logger = logging.getLogger("main.apps.upload.api.share")


@router.get("/{token}")
async def access_shared_file(
    token: str = Path(..., min_length=16, max_length=64),
    service: FileShareLinkService = Depends(get_file_share_link_service),
) -> CustomFileresponse:
    data, filename, media_type, disposition = await service.access_by_token(token)
    return CustomFileresponse(
        data=data,
        filename=filename,
        media_type=media_type,
        content_disposition_type=disposition,
    )

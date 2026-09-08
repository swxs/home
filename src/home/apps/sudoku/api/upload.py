# -*- coding: utf-8 -*-
# @File    : api/upload.py
# @AUTH    : code_creater

import logging

from fastapi import APIRouter, UploadFile
from fastapi.param_functions import Depends

from home.web.response import success
from home.web.schemas.response import SuccessResponse

# 本模块方法
from ..schemas.response import SudokuUploadPreviewResponse
from ..services.sudoku_image_service import (
    SudokuImageService,
    get_sudoku_image_service,
)

router = APIRouter()
logger = logging.getLogger("main.apps.sudoku.api.upload")


@router.post("/preview/", response_model=SuccessResponse[SudokuUploadPreviewResponse])
async def preview_sudoku_image(
    file: UploadFile,
    service: SudokuImageService = Depends(get_sudoku_image_service),
):
    """解析数独图片，仅返回题目与答案字符串，不落库、不校验数独规则（由用户确认后再走创建接口）。"""
    payload = await service.preview(file)
    return success({"data": payload})

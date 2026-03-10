# -*- coding: utf-8 -*-
# @File    : api/upload.py
# @AUTH    : code_creater

import logging
import datetime

from fastapi import APIRouter, UploadFile
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from web.dependencies.db import get_db, get_single_worker
from web.exceptions import Http400BadRequestException
from web.response import success
from web.schemas.response import SuccessResponse

# 本模块方法
from .. import consts
from ..models.sudoku_puzzle import SudokuPuzzle
from ..schemas.response import SudokuPuzzleResponse
from ..schemas.sudoku_puzzle import SudokuPuzzleSchema
from ..utils.image_parser import parse_image_to_sudoku
from ..utils.sudoku_validator import is_valid_sudoku_grid

router = APIRouter()
logger = logging.getLogger("main.apps.sudoku.api.upload")


@router.post("/", response_model=SuccessResponse[SudokuPuzzleResponse])
async def upload_sudoku_image(
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
):
    if file.content_type not in consts.ALLOWED_IMAGE_CONTENT_TYPES:
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "仅支持 image/jpeg 或 image/png",
        )
    data = await file.read()
    if len(data) > consts.MAX_UPLOAD_SIZE:
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            f"图片大小超过限制（最大 {consts.MAX_UPLOAD_SIZE // (1024 * 1024)}MB）",
        )
    try:
        raw = parse_image_to_sudoku(data)
    except Http400BadRequestException:
        raise
    except Exception as e:
        logger.exception("解析数独图片失败")
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            f"解析失败: {e!s}",
        )
    schema = SudokuPuzzleSchema(
        puzzle=raw["puzzle"],
        solution=raw["solution"],
        puzzle_date=datetime.date.today(),
    )
    if not is_valid_sudoku_grid(schema.solution):
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "答案不是合法数独解",
        )
    single_worker = await get_single_worker(db, SudokuPuzzle)
    async with single_worker as worker:
        instance = await worker.repository.create_one(schema)
    return success({"data": SudokuPuzzleSchema.model_validate(instance)})

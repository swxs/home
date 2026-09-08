# -*- coding: utf-8 -*-
# @File    : services/sudoku_image_service.py
# @AUTH    : code_creater

import logging

from fastapi import UploadFile

from home.web.exceptions import Http400BadRequestException

# 本模块方法
from .. import consts
from ..schemas.sudoku_puzzle import SudokuUploadPreviewData
from ..utils.image_parser import parse_image_to_sudoku

logger = logging.getLogger("main.apps.sudoku.services.sudoku_image_service")


class SudokuImageService:
    """数独图片解析业务层：上传图片校验与解析（不落库）。"""

    async def preview(self, file: UploadFile) -> SudokuUploadPreviewData:
        """解析数独图片，仅返回题目与答案字符串，不落库、不校验数独规则（由用户确认后再走创建接口）。"""
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
        return SudokuUploadPreviewData(
            puzzle=raw.get("puzzle") or "",
            solution=raw.get("solution") or "",
        )


async def get_sudoku_image_service() -> SudokuImageService:
    return SudokuImageService()

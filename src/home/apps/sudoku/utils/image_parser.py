# -*- coding: utf-8 -*-
# @File    : utils/image_parser.py
# @AUTH    : code_creater

"""
图片解析为数独 puzzle/solution。
第一阶段：占位实现，返回固定测试题或抛异常。
第二阶段：可替换为 OpenCV + OCR 或第三方 API。
"""

import logging

from home.web.exceptions import Http400BadRequestException

logger = logging.getLogger("main.apps.sudoku.utils.image_parser")

# 用于联调的一道合法数独（题目 + 答案）
_PLACEHOLDER_PUZZLE = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
_PLACEHOLDER_SOLUTION = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"


def parse_image_to_sudoku(image_bytes: bytes) -> dict:
    """
    从图片字节解析出数独题目与答案。

    Args:
        image_bytes: 图片二进制内容（如 JPEG/PNG）

    Returns:
        {"puzzle": str, "solution": str}，均为 81 位字符串

    Raises:
        Http400BadRequestException: 解析失败或未实现时
    """
    if not image_bytes or len(image_bytes) == 0:
        raise Http400BadRequestException(
            Http400BadRequestException.IllegalArgument,
            "图片内容为空",
        )
    # 第一阶段：占位，返回固定题目便于联调；若要强制走“未实现”可改为 raise
    # raise Http400BadRequestException(
    #     Http400BadRequestException.IllegalArgument,
    #     "图片解析功能尚未实现",
    # )
    logger.info("使用占位数独数据（图片解析未实现）")
    return {
        "puzzle": _PLACEHOLDER_PUZZLE,
        "solution": _PLACEHOLDER_SOLUTION,
    }

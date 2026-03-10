# -*- coding: utf-8 -*-
# @FILE    : consts.py
# @AUTH    : model_creater

from enum import IntEnum

# 允许上传的图片类型
ALLOWED_IMAGE_CONTENT_TYPES = ("image/jpeg", "image/png")
# 上传文件最大大小（字节，10MB）
MAX_UPLOAD_SIZE = 10 * 1024 * 1024


class Difficulty(IntEnum):
    """数独难度"""

    EASY = 1
    MEDIUM = 2
    HARD = 3

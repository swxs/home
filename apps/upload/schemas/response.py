# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import Dict, List, TypedDict

from web.schemas.pagination import PaginationSchema

# 本模块方法
from .file_info import FileInfoSchema


class FileInfoSearchResponse(TypedDict):
    data: List[FileInfoSchema]
    pagination: PaginationSchema


class FileInfoResponse(TypedDict):
    data: FileInfoSchema


class FilePathResponse(TypedDict):
    path: str

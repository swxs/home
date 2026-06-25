# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import List, TypedDict

from web.schemas.pagination import PaginationSchema

# 本模块方法
from .file_info import FileInfoOut


class FileInfoSearchResponse(TypedDict):
    data: List[FileInfoOut]
    pagination: PaginationSchema


class FileInfoResponse(TypedDict):
    data: FileInfoOut


class FilePathResponse(TypedDict):
    path: str

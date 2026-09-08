# -*- coding: utf-8 -*-
# @FILE    : schemas/response.py
# @AUTH    : model_creater

from typing import List, TypedDict

from home.web.schemas.pagination import PaginationSchema

# 本模块方法
from .file_info import FileInfoOut
from .file_share_link import FileShareLinkOut


class FileInfoSearchResponse(TypedDict):
    data: List[FileInfoOut]
    pagination: PaginationSchema


class FileInfoResponse(TypedDict):
    data: FileInfoOut


class FilePathResponse(TypedDict):
    path: str


class FileLinkResponse(TypedDict):
    url: str


class FileShareLinkSearchResponse(TypedDict):
    data: List[FileShareLinkOut]
    pagination: PaginationSchema


class FileShareLinkResponse(TypedDict):
    data: FileShareLinkOut

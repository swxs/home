# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import logging
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Body, Path, Query
from fastapi.param_functions import Depends

from web.custom_types import OID
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.search import SearchSchema, get_search
from web.dependencies.token import TokenSchema, get_token
from web.response import success

# 通用方法
from commons.Helpers import oss2_helper

# 本模块方法
from .. import file_info_utils
from ..dao.file_info import FileInfo
from ..schemas.file_info import FileInfoSchema, get_file_info_schema

router = APIRouter()

logger = logging.getLogger("main.apps.password_lock.api.searcher")


@router.post("/")
async def upload_file():
    path = "00/002131231"
    files = oss2_helper.list_dir_files("00")
    file = oss2_helper.upload(path, b"test")
    data = oss2_helper.download(path)
    return success(data={"file": file, "data": data})

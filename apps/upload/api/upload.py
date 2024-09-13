# -*- coding: utf-8 -*-
# @File    : api/password_lock.py
# @AUTH    : code_creater

import io
import os
import hashlib
import logging
from typing import Any

from bson import ObjectId
from fastapi import APIRouter, Body, Path, Query, UploadFile
from fastapi.param_functions import Depends
from fastapi.responses import FileResponse

from web.custom_types import OID
from web.dependencies.pagination import PageSchema, PaginationSchema, get_pagination
from web.dependencies.search import SearchSchema, get_search
from web.dependencies.token import TokenSchema, get_token
from web.response import CustomFileresponse, success

# 通用方法
from commons.Helpers import oss2_helper

# 本模块方法
from .. import consts, file_info_utils
from ..dao.file_info import FileInfo
from ..schemas.file_info import FileInfoSchema, get_file_info_schema

router = APIRouter()

logger = logging.getLogger("main.apps.upload")


@router.post("/")
async def upload_file(file: UploadFile):
    data = await file.read()
    file_id = hashlib.md5(data).hexdigest()
    try:
        oss2_helper.upload(f'{file_id[:4]}/{file_id[4:]}', data)
        file_info = await FileInfo.create(
            params={
                "file_id": file_id,
                "file_name": file.filename,
                "file_size": file.size,
                "ext": os.path.splitext(file.filename)[1],
                "policy": consts.FILE_INFO_POLICY_ALIOSS,
            }
        )
        return success(data=file_info)
    except Exception as e:
        file_info = await FileInfo.find_one(
            finds={"file_id": file_id},
        )
        return success(data=file_info)


@router.get("/download/{file_info_id}")
async def download(
    file_info_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    file_info = await FileInfo.find_one(
        finds={"id": ObjectId(file_info_id)},
    )
    file_id = file_info.file_id
    file_name = file_info.file_name
    return CustomFileresponse(
        data=oss2_helper.download(f'{file_id[:4]}/{file_id[4:]}'),
        filename=file_name,
    )

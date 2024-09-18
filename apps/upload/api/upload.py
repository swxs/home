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
    filename = file.filename if file.filename else "unknown"
    try:
        oss2_helper.upload(f'{file_id[:4]}/{file_id[4:]}', data)
    except Exception as e:
        raise e
    file_info = await FileInfo.create(
        params={
            "file_id": file_id,
            "file_name": filename,
            "file_size": file.size,
            "ext": os.path.splitext(filename)[1],
            "policy": consts.FILE_INFO_POLICY_ALIOSS,
        }
    )
    return success(data=file_info)


@router.get("/{file_info_id}")
async def download_file(
    file_info_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    file_info = await FileInfo.find_one(
        finds={"id": ObjectId(file_info_id)},
        nullable=False,
    )
    return CustomFileresponse(
        data=oss2_helper.download(f'{file_info.file_id[:4]}/{file_info.file_id[4:]}'),
        filename=file_info.file_name,
    )


@router.delete("/{file_info_id}")
async def delete_file(
    file_info_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    file_info = await FileInfo.find_one(
        finds={"id": ObjectId(file_info_id)},
        nullable=False,
    )
    oss2_helper.delete(f'{file_info.file_id[:4]}/{file_info.file_id[4:]}')
    count = await FileInfo.delete_one(finds={"id": ObjectId(file_info_id)})
    return success(
        {
            "count": count,
        }
    )


@router.get("/path/{file_info_id}")
async def path(
    file_info_id: OID = Path(..., regex="[0-9a-f]{24}"),
):
    file_info = await FileInfo.find_one(
        finds={"id": ObjectId(file_info_id)},
        nullable=False,
    )

    return success(
        data={
            "path": oss2_helper.get_sign_download_path(
                f'{file_info.file_id[:4]}/{file_info.file_id[4:]}',
                file_info.file_name,
            ),
        },
    )

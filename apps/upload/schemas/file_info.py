# -*- coding: utf-8 -*-
# @FILE    : schemas/file_info.py
# @AUTH    : model_creater

from typing import Optional

from fastapi import Query

from web.schemas import BaseSchema


class _FileInfoFields(BaseSchema):
    """文件信息字段集合，供各用途 schema 复用。"""

    file_id: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    ext: Optional[str] = None
    policy: Optional[int] = None


class FileInfoFilter(_FileInfoFields):
    """列表查询过滤条件。"""


class FileInfoCreate(_FileInfoFields):
    """创建入参。"""


class FileInfoUpdate(_FileInfoFields):
    """更新入参。"""


class FileInfoOut(_FileInfoFields):
    """输出 DTO。"""


async def get_file_info_filter(
    file_id: Optional[str] = Query(None),
    file_name: Optional[str] = Query(None),
    file_size: Optional[str] = Query(None),
    ext: Optional[str] = Query(None),
    policy: Optional[str] = Query(None),
) -> FileInfoFilter:
    params = {}
    if file_id is not None:
        params["file_id"] = file_id
    if file_name is not None:
        params["file_name"] = file_name
    if file_size is not None:
        params["file_size"] = file_size
    if ext is not None:
        params["ext"] = ext
    if policy is not None:
        params["policy"] = policy

    return FileInfoFilter(**params)

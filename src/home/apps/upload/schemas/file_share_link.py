# -*- coding: utf-8 -*-
# @FILE    : schemas/file_share_link.py
# @AUTH    : code_creater

from datetime import datetime
from typing import Optional

from fastapi import Query

from home.web.schemas import BaseSchema


class _FileShareLinkFields(BaseSchema):
    file_info_id: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    expires_at: Optional[datetime] = None
    status: Optional[int] = None
    token: Optional[str] = None
    create_by: Optional[str] = None


class FileShareLinkFilter(_FileShareLinkFields):
    """列表查询过滤条件。"""


class FileShareLinkCreate(BaseSchema):
    file_info_id: str
    name: str
    description: Optional[str] = None
    expires_at: Optional[datetime] = None


class FileShareLinkPersist(FileShareLinkCreate):
    token: str
    create_by: str
    status: int


class FileShareLinkUpdate(BaseSchema):
    status: Optional[int] = None


class FileShareLinkOut(_FileShareLinkFields):
    id: Optional[str] = None
    create_at: Optional[datetime] = None
    update_at: Optional[datetime] = None
    url: Optional[str] = None
    file_name: Optional[str] = None


async def get_file_share_link_filter(
    file_info_id: Optional[str] = Query(None),
    name: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
) -> FileShareLinkFilter:
    params = {}
    if file_info_id is not None:
        params["file_info_id"] = file_info_id
    if name is not None:
        params["name"] = name
    if status is not None:
        params["status"] = status

    return FileShareLinkFilter(**params)

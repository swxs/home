# -*- coding: utf-8 -*-
# @FILE    : schemas/file_info.py
# @AUTH    : model_creater

from typing import Optional

from fastapi import Query
from pydantic import Field, field_validator

from web.schemas import BaseSchema


class _FileInfoFields(BaseSchema):
    """文件信息字段集合，供各用途 schema 复用。"""

    file_id: Optional[str] = Field(None, pattern=r"^[0-9a-f]{32}$")
    file_name: Optional[str] = Field(None, min_length=1, max_length=255)
    file_size: Optional[int] = Field(None, ge=0)
    ext: Optional[str] = None
    policy: Optional[int] = None


class FileInfoFilter(_FileInfoFields):
    """列表查询过滤条件。"""

    user_id: Optional[str] = None


class FileInfoPersist(BaseSchema):
    """仅供服务层持久化使用，客户端不能直接构造归属。"""

    user_id: str
    file_id: str = Field(pattern=r"^[0-9a-f]{32}$")
    file_name: str = Field(min_length=1, max_length=255)
    file_size: int = Field(ge=0)
    ext: Optional[str] = Field(None, max_length=50)
    policy: int

    @field_validator("file_id")
    @classmethod
    def normalize_file_id(cls, value: str) -> str:
        return value.lower()


class FileInfoUpdate(BaseSchema):
    """仅允许修改展示元数据，禁止改内容身份和归属。"""

    file_name: Optional[str] = Field(None, min_length=1, max_length=255)
    ext: Optional[str] = Field(None, max_length=50)


class FileInfoOut(_FileInfoFields):
    """输出 DTO。"""

    user_id: Optional[str] = None


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

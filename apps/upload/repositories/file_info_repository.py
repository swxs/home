# -*- coding: utf-8 -*-
# @File    : repositories/file_info_repository.py
# @AUTH    : code_creater

from sqlalchemy.ext.asyncio import AsyncSession

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.file_info import FileInfo


class FileInfoRepository(BaseRepository[FileInfo]):
    """
    文件信息Repository
    可以在这里添加FileInfo特定的查询方法
    """

    model = FileInfo
    name = "file_info"

    filterable_fields = {"file_id", "file_name", "file_size", "ext", "policy"}
    sortable_fields = {"id", "create_at", "update_at", "file_name", "file_size", "ext"}

    # 如果需要FileInfo特定的方法，可以在这里添加

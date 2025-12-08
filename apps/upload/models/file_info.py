# -*- coding: utf-8 -*-
# @FILE    : models/file_info.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel
from mysqlengine.fields import IntEnumType

# 本模块方法
from .. import consts


class FileInfo(baseModel):
    __tablename__ = "file_info"  # 数据库表名
    file_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="文件ID",
    )
    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="文件名",
    )
    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="文件大小",
    )
    ext: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="文件扩展名",
    )
    policy: Mapped[consts.FileInfo_Policy] = mapped_column(
        IntEnumType(consts.FileInfo_Policy),
        nullable=False,
        comment="存储策略",
    )

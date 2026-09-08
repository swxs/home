# -*- coding: utf-8 -*-
# @FILE    : models/file_info.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from home.mysqlengine import baseModel
from home.mysqlengine.fields import IntEnumType, ObjectIdType
from home.web.schemas.types import objectId

# 本模块方法
from .. import consts


class FileInfo(baseModel):
    __tablename__ = "file_info"  # 数据库表名
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "file_id",
            "file_size",
            name="uq_file_info_user_content",
        ),
        Index("idx_file_info_user_id", "user_id"),
        Index("idx_file_info_content", "file_id", "file_size"),
    )

    user_id: Mapped[objectId] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="所属用户ID",
    )
    file_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
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

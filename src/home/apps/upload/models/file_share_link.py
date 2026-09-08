# -*- coding: utf-8 -*-
# @FILE    : models/file_share_link.py
# @AUTH    : code_creater

from datetime import datetime
from typing import Optional

from sqlalchemy import Index, String, Text, UniqueConstraint
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import Mapped, mapped_column

from home.mysqlengine import baseModel
from home.mysqlengine.fields import IntEnumType, ObjectIdType
from home.web.schemas.types import objectId

# 本模块方法
from .. import consts


class FileShareLink(baseModel):
    __tablename__ = "file_share_link"
    __table_args__ = (
        UniqueConstraint("token", name="uq_file_share_link_token"),
        Index("idx_file_share_link_file_info_id", "file_info_id"),
        Index("idx_file_share_link_create_by", "create_by"),
    )

    token: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        comment="分享 token",
    )
    file_info_id: Mapped[objectId] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="文件信息 ID",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="链接名称",
    )
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="备注",
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DATETIME(fsp=6),
        nullable=True,
        comment="过期时间",
    )
    status: Mapped[consts.ShareLinkStatus] = mapped_column(
        IntEnumType(consts.ShareLinkStatus),
        nullable=False,
        default=consts.ShareLinkStatus.ACTIVE,
        comment="链接状态",
    )

# -*- coding: utf-8 -*-
# @FILE    : models/oauth_client.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel
from mysqlengine.fields import IntEnumType, ObjectIdType
from web.custom_types import objectId

# 本模块方法
from .. import consts


class OAuthClient(baseModel):
    __tablename__ = "oauth_client"  # 数据库表名
    client_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="客户端ID",
    )
    client_secret: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="客户端密钥",
    )
    client_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="客户端名称",
    )
    redirect_uri: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="重定向URI",
    )
    user_id: Mapped[Optional[objectId]] = mapped_column(
        ObjectIdType,
        nullable=True,
        comment="所属用户ID",
    )
    is_active: Mapped[consts.OAuthClient_IsActive] = mapped_column(
        IntEnumType(consts.OAuthClient_IsActive),
        default=consts.OAuthClient_IsActive.ACTIVE,
        nullable=False,
        comment="是否激活",
    )

    __table_args__ = (
        Index("idx_client_id", "client_id"),
        Index("idx_user_id", "user_id"),
    )

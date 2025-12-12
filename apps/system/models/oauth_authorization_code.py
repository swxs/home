# -*- coding: utf-8 -*-
# @FILE    : models/oauth_authorization_code.py
# @AUTH    : code_creater

from datetime import datetime

from sqlalchemy import DateTime, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel
from mysqlengine.fields import ObjectIdType
from web.custom_types import objectId


class OAuthAuthorizationCode(baseModel):
    __tablename__ = "oauth_authorization_code"  # 数据库表名
    code: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        comment="授权码",
    )
    client_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="客户端ID",
    )
    user_id: Mapped[objectId] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="用户ID",
    )
    redirect_uri: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        comment="重定向URI",
    )
    scope: Mapped[str] = mapped_column(
        String(500),
        nullable=True,
        comment="授权范围",
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        comment="过期时间",
    )
    is_used: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
        comment="是否已使用",
    )

    __table_args__ = (
        Index("idx_code", "code"),
        Index("idx_client_id", "client_id"),
        Index("idx_user_id", "user_id"),
    )

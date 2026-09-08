# -*- coding: utf-8 -*-
# @FILE    : models/oauth_user_grant.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import Index, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from home.mysqlengine import baseModel
from home.mysqlengine.fields import ObjectIdType
from home.web.custom_types import objectId


class OAuthUserGrant(baseModel):
    __tablename__ = "oauth_user_grant"
    user_id: Mapped[objectId] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="用户ID",
    )
    client_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="客户端ID",
    )
    scope: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
        comment="授权范围",
    )

    __table_args__ = (
        UniqueConstraint("user_id", "client_id", name="uq_oauth_user_grant_user_client"),
        Index("idx_oauth_user_grant_user_id", "user_id"),
        Index("idx_oauth_user_grant_client_id", "client_id"),
    )

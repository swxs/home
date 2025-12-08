# -*- coding: utf-8 -*-
# @FILE    : models/user.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel
from mysqlengine.fields import IntEnumType, ObjectIdType
from web.custom_types import objectId

# 本模块方法
from .. import consts


class UserAuth(baseModel):
    __tablename__ = "user_auth"  # 数据库表名
    user_id: Mapped[objectId] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="用户ID",
    )
    ttype: Mapped[consts.UserAuth_Ttype] = mapped_column(
        IntEnumType(consts.UserAuth_Ttype),
        default=consts.UserAuth_Ttype.PASSWORD,
        nullable=False,
        comment="认证类型",
    )
    identifier: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="认证标识",
    )
    credential: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="认证凭证",
    )
    ifverified: Mapped[consts.UserAuth_Ifverified] = mapped_column(
        IntEnumType(consts.UserAuth_Ifverified),
        default=consts.UserAuth_Ifverified.UNVERIFIED,
        nullable=False,
        comment="认证状态",
    )

    __table_args__ = (
        Index("idx_user_id_ttype", "user_id", "ttype"),
        Index("idx_ttype_identifier", "ttype", "identifier", unique=True),
    )

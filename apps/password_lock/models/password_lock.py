# -*- coding: utf-8 -*-
# @FILE    : models/password_lock.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import JSON, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel
from mysqlengine.fields import IntEnumType, ObjectIdType
from web.custom_types import objectId

# 本模块方法
from .. import consts
from ..schemas.password_lock import PasswordLockCustom


class PasswordLock(baseModel):
    __tablename__ = "password_lock"  # 数据库表名
    user_id: Mapped[objectId] = mapped_column(
        ObjectIdType,
        nullable=False,
        comment="用户ID",
    )
    key: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="标识",
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="名称",
    )
    website: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="网址",
    )
    used: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="使用计数",
    )
    ttype: Mapped[consts.PasswordLock_Ttype] = mapped_column(
        IntEnumType(consts.PasswordLock_Ttype),
        default=consts.PasswordLock_Ttype.COMMON,
        nullable=False,
        comment="类型",
    )
    custom: Mapped[Optional[PasswordLockCustom]] = mapped_column(
        JSON,
        nullable=True,
        comment="自定义数据",
    )

    __table_args__ = (Index("idx_user_id_key", "user_id", "key", unique=True),)

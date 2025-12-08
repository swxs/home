# -*- coding: utf-8 -*-
# @FILE    : models/user.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel
from mysqlengine.fields import ObjectIdType


class User(baseModel):
    __tablename__ = "user"  # 数据库表名
    username: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
        comment="用户姓名",
    )
    description: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="个人备注",
    )
    avatar: Mapped[Optional[str]] = mapped_column(
        ObjectIdType,
        nullable=True,
        comment="头像文件ID",
    )

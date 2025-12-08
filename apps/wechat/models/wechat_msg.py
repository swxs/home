# -*- coding: utf-8 -*-
# @FILE    : models/wechat_msg.py
# @AUTH    : code_creater

from typing import Optional

from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from mysqlengine import baseModel


class WechatMsg(baseModel):
    __tablename__ = "wechat_msg"  # 数据库表名
    msg_id: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="消息ID",
    )
    msg_type: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="消息类型",
    )
    msg_event: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="消息事件",
    )
    msg: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="消息内容",
    )

    __table_args__ = (Index("idx_msg_id", "msg_id"),)

# -*- coding: utf-8 -*-

from typing import Optional

from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from home.mysqlengine import baseModel
from home.mysqlengine.fields import IntEnumType

# 本模块方法
from ...consts import EmailSendStatus, EmailTemplateType


class EmailSendRecord(baseModel):
    __tablename__ = "email_send_record"

    recipient: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="收件人邮箱",
    )
    subject: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="邮件主题",
    )
    template_type: Mapped[EmailTemplateType] = mapped_column(
        String(50),
        nullable=False,
        comment="模板类型",
    )
    body: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="邮件正文快照",
    )
    status: Mapped[EmailSendStatus] = mapped_column(
        IntEnumType(EmailSendStatus),
        default=EmailSendStatus.PENDING,
        nullable=False,
        comment="发送状态",
    )
    error: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="失败原因",
    )

    __table_args__ = (Index("idx_recipient_template", "recipient", "template_type"),)

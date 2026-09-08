# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import Query

from home.web.schemas import BaseSchema

# 本模块方法
from ...consts import EmailSendStatus, EmailTemplateType


class _EmailSendRecordFields(BaseSchema):
    recipient: Optional[str] = None
    subject: Optional[str] = None
    template_type: Optional[EmailTemplateType] = None
    body: Optional[str] = None
    status: Optional[EmailSendStatus] = None
    error: Optional[str] = None


class EmailSendRecordFilter(_EmailSendRecordFields):
    pass


class EmailSendRecordCreate(_EmailSendRecordFields):
    pass


class EmailSendRecordUpdate(_EmailSendRecordFields):
    pass


class EmailSendRecordOut(_EmailSendRecordFields):
    pass


async def get_email_send_record_filter(
    recipient: Optional[str] = Query(None),
    template_type: Optional[str] = Query(None),
    status: Optional[int] = Query(None),
) -> EmailSendRecordFilter:
    params = {}
    if recipient is not None:
        params["recipient"] = recipient
    if template_type is not None:
        params["template_type"] = template_type
    if status is not None:
        params["status"] = status
    return EmailSendRecordFilter(**params)

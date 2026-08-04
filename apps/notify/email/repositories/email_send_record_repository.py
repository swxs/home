# -*- coding: utf-8 -*-

from mysqlengine.repositories import BaseRepository

# 本模块方法
from ..models.email_send_record import EmailSendRecord


class EmailSendRecordRepository(BaseRepository[EmailSendRecord]):
    model = EmailSendRecord
    name = "email_send_record"

    filterable_fields = {"recipient", "subject", "template_type", "status"}
    sortable_fields = {"id", "create_at", "update_at", "recipient", "status"}

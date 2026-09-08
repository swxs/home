from home.web.schemas.types import objectId
# -*- coding: utf-8 -*-
"""邮件发送后台任务：脱离 HTTP 请求生命周期，仅使用 mysqlengine session 原语。"""

import logging

from home.mysqlengine import open_session, transaction

from ...consts import EmailSendStatus
from ..channel import send_email
from ..repositories.email_send_record_repository import EmailSendRecordRepository
from ..schemas.email_send_record import EmailSendRecordUpdate

logger = logging.getLogger("main.apps.notify.email.tasks.send_email_task")


async def send_email_record_task(
    record_id: objectId,
    to: str,
    subject: str,
    html_body: str,
    text_body: str,
) -> None:
    async with open_session() as session:
        repo = EmailSendRecordRepository(session)
        try:
            send_email(to, subject, html_body, text_body)
            async with transaction(session):
                await repo.update_one(
                    record_id,
                    EmailSendRecordUpdate(status=EmailSendStatus.SENT),
                )
        except Exception as exc:
            logger.error("邮件发送失败 record_id=%s: %s", record_id, exc, exc_info=True)
            async with transaction(session):
                await repo.update_one(
                    record_id,
                    EmailSendRecordUpdate(status=EmailSendStatus.FAILED, error=str(exc)),
                )

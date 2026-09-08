# -*- coding: utf-8 -*-

import logging
from typing import Optional

from fastapi import BackgroundTasks
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import home.core as core
from home.mysqlengine import SessionLocal
from home.web.dependencies.db import get_db
from home.web.dependencies.transaction import transaction

# 本模块方法
from ...consts import EmailSendStatus, EmailTemplateType
from ...utils.rate_limit import check_and_record_send
from ..channel import send_email
from ..repositories.email_send_record_repository import EmailSendRecordRepository
from ..schemas.email_send_record import EmailSendRecordCreate, EmailSendRecordUpdate
from ..templates import render_email

logger = logging.getLogger("main.apps.notify.email.services.email_send_service")


class EmailSendService:
    def __init__(self, db: AsyncSession, repo: Optional[EmailSendRecordRepository] = None):
        self.db = db
        self.repo = repo or EmailSendRecordRepository(db)

    def _build_action_url(self, template_type: EmailTemplateType, token: str) -> str:
        base = core.config.OAUTH2_LOGIN_URL.rstrip("/")
        if template_type == EmailTemplateType.EMAIL_VERIFY:
            return f"{base}/verify-email?token={token}"
        return f"{base}/reset-password?token={token}"

    async def schedule_send(
        self,
        background_tasks: BackgroundTasks,
        template_type: EmailTemplateType,
        to: str,
        token: str,
    ) -> None:
        await check_and_record_send(to, template_type.value)
        action_url = self._build_action_url(template_type, token)
        subject, html_body, text_body = render_email(template_type, action_url)

        async with transaction(self.db):
            record = await self.repo.create_one(
                EmailSendRecordCreate(
                    recipient=to,
                    subject=subject,
                    template_type=template_type,
                    body=html_body,
                    status=EmailSendStatus.PENDING,
                )
            )

        record_id = str(record.id)
        background_tasks.add_task(
            _send_in_background,
            record_id,
            to,
            subject,
            html_body,
            text_body,
        )


async def _send_in_background(
    record_id: str,
    to: str,
    subject: str,
    html_body: str,
    text_body: str,
) -> None:
    async with SessionLocal() as db:
        repo = EmailSendRecordRepository(db)
        try:
            send_email(to, subject, html_body, text_body)
            async with transaction(db):
                await repo.update_one(
                    record_id,
                    EmailSendRecordUpdate(status=EmailSendStatus.SENT),
                )
        except Exception as exc:
            logger.error("邮件发送失败 record_id=%s: %s", record_id, exc, exc_info=True)
            async with transaction(db):
                await repo.update_one(
                    record_id,
                    EmailSendRecordUpdate(status=EmailSendStatus.FAILED, error=str(exc)),
                )


async def get_email_send_service(db: AsyncSession = Depends(get_db)) -> EmailSendService:
    return EmailSendService(db)

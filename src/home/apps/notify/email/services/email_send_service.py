# -*- coding: utf-8 -*-

import logging
from typing import Optional

from fastapi import BackgroundTasks
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

import home.core as core
from home.web.dependencies.session import get_session, transaction

# 本模块方法
from ...consts import EmailSendStatus, EmailTemplateType
from ...utils.rate_limit import check_and_record_send
from ..repositories.email_send_record_repository import EmailSendRecordRepository
from ..schemas.email_send_record import EmailSendRecordCreate
from ..tasks import send_email_record_task
from ..templates import render_email

logger = logging.getLogger("main.apps.notify.email.services.email_send_service")


class EmailSendService:
    def __init__(self, session: AsyncSession, repo: Optional[EmailSendRecordRepository] = None):
        self.session = session
        self.repo = repo or EmailSendRecordRepository(session)

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

        async with transaction(self.session):
            record = await self.repo.create_one(
                EmailSendRecordCreate(
                    recipient=to,
                    subject=subject,
                    template_type=template_type,
                    body=html_body,
                    status=EmailSendStatus.PENDING,
                )
            )

        background_tasks.add_task(
            send_email_record_task,
            str(record.id),
            to,
            subject,
            html_body,
            text_body,
        )


async def get_email_send_service(session: AsyncSession = Depends(get_session)) -> EmailSendService:
    return EmailSendService(session)

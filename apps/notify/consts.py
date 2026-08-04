# -*- coding: utf-8 -*-

from enum import IntEnum, StrEnum


class EmailTemplateType(StrEnum):
    EMAIL_VERIFY = "email_verify"
    PASSWORD_RESET = "password_reset"


class EmailSendStatus(IntEnum):
    PENDING = 1
    SENT = 2
    FAILED = 3


class TokenPurpose(StrEnum):
    EMAIL_VERIFY = "email_verify"
    PASSWORD_RESET = "password_reset"

# -*- coding: utf-8 -*-

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class VerifyEmailRequest(BaseModel):
    token: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=20)
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6, max_length=128)


class MessageResponse(BaseModel):
    message: str
    unactivated: bool = False

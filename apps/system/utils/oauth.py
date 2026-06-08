# -*- coding: utf-8 -*-
# @FILE    : utils/oauth.py
# @AUTH    : code_creater

import secrets
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode

import core

DEFAULT_SCOPE = "read write"


def normalize_scope(scope: Optional[str]) -> str:
    """统一 scope 格式，避免空值或顺序不同导致匹配失败"""
    if not scope or not scope.strip():
        return DEFAULT_SCOPE
    return " ".join(sorted(scope.strip().split()))


def generate_authorization_code() -> str:
    """生成授权码（32字节的随机字符串）"""
    return secrets.token_urlsafe(32)


def get_authorization_code_expires_at() -> datetime:
    """获取授权码过期时间（10分钟后）"""
    return datetime.utcnow() + timedelta(minutes=10)


def validate_redirect_uri(client_redirect_uri: str, request_redirect_uri: str) -> bool:
    """验证重定向URI是否匹配"""
    # 简单的字符串匹配，可以根据需要增强（支持通配符等）
    return client_redirect_uri == request_redirect_uri


def build_authorization_url(redirect_uri: str, code: str, state: Optional[str] = None) -> str:
    """构建授权重定向URL"""
    params = {"code": code}
    if state:
        params["state"] = state

    separator = "&" if "?" in redirect_uri else "?"
    return f"{redirect_uri}{separator}{urlencode(params)}"


def build_error_redirect_url(redirect_uri: str, error: str, error_description: str, state: Optional[str] = None) -> str:
    """构建错误重定向URL"""
    params = {
        "error": error,
        "error_description": error_description,
    }
    if state:
        params["state"] = state

    separator = "&" if "?" in redirect_uri else "?"
    return f"{redirect_uri}{separator}{urlencode(params)}"


def build_consent_redirect_url(
    client_id: str,
    redirect_uri: str,
    response_type: str = "code",
    scope: Optional[str] = None,
    state: Optional[str] = None,
) -> str:
    """构建授权确认页 URL（openapi_auth /authorize）"""
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": response_type,
    }
    if scope:
        params["scope"] = scope
    if state:
        params["state"] = state

    consent_base = core.config.OAUTH2_LOGIN_URL.rstrip("/")
    return f"{consent_base}/authorize?{urlencode(params)}"

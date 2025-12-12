# -*- coding: utf-8 -*-
# @FILE    : utils/oauth.py
# @AUTH    : code_creater

import secrets
from datetime import datetime, timedelta
from typing import Optional
from urllib.parse import urlencode


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

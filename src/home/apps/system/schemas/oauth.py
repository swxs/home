# -*- coding: utf-8 -*-
# @FILE    : schemas/oauth.py
# @AUTH    : code_creater

from typing import Optional

from pydantic import BaseModel


class OAuthAuthorizationRequest(BaseModel):
    """OAuth授权请求参数"""

    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: Optional[str] = None
    state: Optional[str] = None


class OAuthTokenRequest(BaseModel):
    """OAuth令牌请求参数"""

    grant_type: str
    code: Optional[str] = None
    redirect_uri: Optional[str] = None
    client_id: str
    client_secret: str
    refresh_token: Optional[str] = None


class OAuthTokenResponse(BaseModel):
    """OAuth令牌响应"""

    access_token: str
    token_type: str = "Bearer"
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class OAuthUserInfoResponse(BaseModel):
    """OAuth用户信息响应"""

    user_id: str
    username: Optional[str] = None

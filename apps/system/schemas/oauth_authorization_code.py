# -*- coding: utf-8 -*-
# @FILE    : schemas/oauth_authorization_code.py
# @AUTH    : model_creater

from datetime import datetime
from typing import Optional

from web.custom_types import objectId
from web.schemas import BaseSchema


class OAuthAuthorizationCodeSchema(BaseSchema):
    code: Optional[str] = None
    client_id: Optional[str] = None
    user_id: Optional[objectId] = None
    redirect_uri: Optional[str] = None
    scope: Optional[str] = None
    expires_at: Optional[datetime] = None
    is_used: Optional[bool] = None

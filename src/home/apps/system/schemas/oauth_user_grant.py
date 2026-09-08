# -*- coding: utf-8 -*-
# @FILE    : schemas/oauth_user_grant.py
# @AUTH    : code_creater

from typing import Optional

from home.web.schemas.types import objectId
from home.web.schemas import BaseSchema


class OAuthUserGrantSchema(BaseSchema):
    user_id: Optional[objectId] = None
    client_id: Optional[str] = None
    scope: Optional[str] = None

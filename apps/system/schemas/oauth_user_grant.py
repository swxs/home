# -*- coding: utf-8 -*-
# @FILE    : schemas/oauth_user_grant.py
# @AUTH    : code_creater

from typing import Optional

from web.custom_types import objectId
from web.schemas import BaseSchema


class OAuthUserGrantSchema(BaseSchema):
    user_id: Optional[objectId] = None
    client_id: Optional[str] = None
    scope: Optional[str] = None

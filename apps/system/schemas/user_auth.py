# -*- coding: utf-8 -*-
# @FILE    : schemas/user_auth.py
# @AUTH    : model_creater

from typing import Dict, List, Optional

from pydantic import BaseModel


class UserAuthSchema(BaseModel):
    user_id: Optional[str] = None
    ttype: Optional[int] = 0
    identifier: Optional[str] = None
    credential: Optional[str] = None
    ifverified: Optional[int] = 0

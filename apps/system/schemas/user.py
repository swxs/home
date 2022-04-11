# -*- coding: utf-8 -*-
# @FILE    : schemas/user.py
# @AUTH    : model_creater

from typing import Dict, List, Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    username: Optional[str] = None
    description: Optional[str] = None
    avatar: Optional[str] = None

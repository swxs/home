# -*- coding: utf-8 -*-
# @FILE    : schemas/word.py
# @AUTH    : model_creater

from typing import Dict, List, Optional

from pydantic import BaseModel


class WordSchema(BaseModel):
    en: Optional[str] = None
    cn: Optional[str] = None
    number: Optional[int] = 0
    last_time: Optional[str] = None
    user_id: Optional[str] = None

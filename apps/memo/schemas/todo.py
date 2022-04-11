# -*- coding: utf-8 -*-
# @FILE    : schemas/todo.py
# @AUTH    : model_creater

from typing import Dict, List, Optional

from pydantic import BaseModel


class TodoSchema(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    document: Optional[str] = None
    user_id: Optional[str] = None
    status: Optional[int] = 0
    priority: Optional[int] = 0
    user_id: Optional[str] = None

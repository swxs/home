# -*- coding: utf-8 -*-
# @File    : Word.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Word import *
from ...BaseModel import BaseModelDocument
from settings import instance


@instance.register
class Word(BaseModelDocument):
    en = fields.StringField(allow_none=True)
    cn = fields.StringField(allow_none=True)
    number = fields.IntField(allow_none=True, default=0)
    last_time = fields.DateTimeField(allow_none=True)

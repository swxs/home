# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.ValueGroup import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class ValueGroup(BaseModelDocument):
    name = fields.StringField(allow_none=True)
    value = fields.IntField(allow_none=True)
    expression = fields.StringField(allow_none=True)


NAME_DICT["ValueGroup"] = ValueGroup

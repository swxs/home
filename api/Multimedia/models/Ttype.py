# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Ttype import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Ttype(BaseModelDocument):
    name = fields.StringField(allow_none=True)


NAME_DICT["Ttype"] = Ttype

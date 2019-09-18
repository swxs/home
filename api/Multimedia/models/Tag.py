# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Tag import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Tag(BaseModelDocument):
    name = fields.StringField(allow_none=True)
    color = fields.StringField(allow_none=True)


NAME_DICT["Tag"] = Tag

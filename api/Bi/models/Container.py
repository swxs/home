# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Container import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Container(BaseModelDocument):
    name = fields.StringField(allow_none=True)
    show_name = fields.BooleanField(allow_none=True, default=False)

    class Meta:
        allow_inheritance = True
        pass


NAME_DICT["Container"] = Container

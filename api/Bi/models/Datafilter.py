# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Datafilter import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Datafilter(BaseModelDocument):
    name = fields.StringField(allow_none=True)
    column_id = fields.ObjectIdField(allow_none=True)
    worktable_id = fields.ObjectIdField(allow_none=True)
    dtype = fields.IntField(allow_none=True, enums=DATAFILTER_DTYPE_LIST)
    custom_attr = fields.DictField(allow_none=True)


NAME_DICT["Datafilter"] = Datafilter

# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Datasource import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Datasource(BaseModelDocument):
    name = fields.StringField(allow_none=True)

    class Meta:
        allow_inheritance = True
        pass


NAME_DICT["Datasource"] = Datasource

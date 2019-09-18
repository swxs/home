# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Datamerge import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Datamerge(BaseModelDocument):
    source_worktable_id = fields.ObjectIdField(allow_none=True)
    source_column_id_list = fields.ListField(fields.StringField(), allow_none=True)
    remote_worktable_id = fields.ObjectIdField(allow_none=True)
    remote_column_id_list = fields.ListField(fields.StringField(), allow_none=True)
    how = fields.IntField(allow_none=True, enums=DATAMERGE_HOW_LIST, default=DATAMERGE_HOW_LEFT)


NAME_DICT["Datamerge"] = Datamerge

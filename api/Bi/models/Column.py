# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Column import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Column(BaseModelDocument):
    col = fields.StringField(allow_none=True)
    realcol = fields.StringField(allow_none=True)
    readablecol = fields.StringField(allow_none=True)
    worktable_id = fields.ObjectIdField(allow_none=True)
    is_visible = fields.BooleanField(allow_none=True, default=True)
    is_unique = fields.BooleanField(allow_none=True, default=False)
    dtype = fields.IntField(allow_none=True, enums=COLUMN_DTYPE_LIST)
    ttype = fields.IntField(allow_none=True, enums=COLUMN_TTYPE_LIST, default=COLUMN_TTYPE_NORMAL)
    expression = fields.StringField(allow_none=True)
    value_group_id_list = fields.StringField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['col', 'worktable_id'],
                'unique': True,
            },
            {
                'key': ['readablecol', 'worktable_id'],
                'unique': True,
            },
        ]
        pass


NAME_DICT["Column"] = Column

# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Column import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Column(BaseModelDocument):
    col = model.StringField()
    realcol = model.StringField()
    readablecol = model.StringField()
    worktable_id = model.ObjectIdField()
    is_visible = model.BooleanField(default=True)
    is_unique = model.BooleanField(default=False)
    dtype = model.IntField(enums=COLUMN_DTYPE_LIST)
    ttype = model.IntField(enums=COLUMN_TTYPE_LIST, default=COLUMN_TTYPE_NORMAL)
    expression = model.StringField()
    value_group_id_list = model.StringField()

    meta = {
        'indexes': [
            {
                'fields': ['col', 'worktable_id'],
                'unique ': True,
            },
            {
                'fields': ['readablecol', 'worktable_id'],
                'unique ': True,
            },
        ],
    }


NAME_DICT["Column"] = Column

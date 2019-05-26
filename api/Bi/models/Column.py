# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Column import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Column(BaseModelDocument):
    col = model.StringField(helper_text='真正的列名')
    realcol = model.StringField(helper_text='原始未处理的列名')
    readablecol = model.StringField(helper_text='展示的列名')
    worktable_id = model.ObjectIdField(helper_text='工作表id')
    is_visible = model.BooleanField(default=True, helper_text='是否可见')
    is_unique = model.BooleanField(default=False, helper_text='是否唯一字段')
    dtype = model.IntField(enums=COLUMN_DTYPE_LIST)
    ttype = model.IntField(enums=COLUMN_TTYPE_LIST, default=COLUMN_TTYPE_NORMAL)
    expression = model.StringField(helper_text='表达式')
    value_group_id_list = model.StringField(helper_text='分组字段id')

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

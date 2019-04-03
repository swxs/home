# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine as model
from ..consts.Worktable import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Worktable(BaseModelDocument):
    name = model.StringField(helper_text='名称')
    datasource_id = model.ObjectIdField()
    engine = model.IntField(enums=WORKTABLE_ENGINE_LIST, default=WORKTABLE_ENGINE_PANDAS)
    status = model.IntField(enums=WORKTABLE_STATUS_LIST, default=WORKTABLE_STATUS_USE)
    description = model.StringField(helper_text='描述')

    meta = {
        'indexes': [
            {
                'fields': ['datasource_id'],
            },
        ]
    }

NAME_DICT["Worktable"] = Worktable

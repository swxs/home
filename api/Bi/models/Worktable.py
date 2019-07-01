# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Worktable import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class Worktable(BaseModelDocument):
    name = model.StringField()
    datasource_id = model.ObjectIdField()
    engine = model.IntField(enums=WORKTABLE_ENGINE_LIST, default=WORKTABLE_ENGINE_PANDAS)
    status = model.IntField(enums=WORKTABLE_STATUS_LIST, default=WORKTABLE_STATUS_USE)
    description = model.StringField()

    meta = {
        'indexes': [
            {
                'fields': ['datasource_id'],
            },
        ],
    }


NAME_DICT["Worktable"] = Worktable

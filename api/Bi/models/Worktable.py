# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Worktable import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Worktable(BaseModelDocument):
    name = fields.StringField(allow_none=True)
    datasource_id = fields.ObjectIdField(allow_none=True)
    engine = fields.IntField(allow_none=True, enums=WORKTABLE_ENGINE_LIST, default=WORKTABLE_ENGINE_PANDAS)
    status = fields.IntField(allow_none=True, enums=WORKTABLE_STATUS_LIST, default=WORKTABLE_STATUS_USE)
    description = fields.StringField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['datasource_id'],
            },
        ]
        pass


NAME_DICT["Worktable"] = Worktable

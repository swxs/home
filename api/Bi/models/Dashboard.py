# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Dashboard import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Dashboard(BaseModelDocument):
    user_id = fields.ObjectIdField(allow_none=True)
    usage = fields.StringField(allow_none=True)
    container_id = fields.ObjectIdField(allow_none=True)
    worktable_id = fields.ObjectIdField(allow_none=True)
    index = fields.IntField(allow_none=True)
    name = fields.StringField(allow_none=True)
    description = fields.StringField(allow_none=True)
    simulate_region_id = fields.ObjectIdField(allow_none=True)
    parent_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['user_id'],
            },
            {
                'key': ['simulate_region_id'],
            },
        ]
        pass


NAME_DICT["Dashboard"] = Dashboard

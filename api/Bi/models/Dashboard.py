# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine as model
from ..consts.Dashboard import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Dashboard(BaseModelDocument):
    user_id = model.ObjectIdField()
    usage = model.StringField()
    container_id = model.ObjectIdField()
    worktable_id = model.ObjectIdField()
    index = model.IntField()
    name = model.StringField()
    description = model.StringField()
    simulate_region_id = model.ObjectIdField()
    parent_id = model.ObjectIdField()

    meta = {
        'indexes': [
            {
                'fields': ['user_id'],
            },
            {
                'fields': ['simulate_region_id'],
            },
        ]
    }

NAME_DICT["Dashboard"] = Dashboard

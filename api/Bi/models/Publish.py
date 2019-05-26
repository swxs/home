# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Publish import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Publish(BaseModelDocument):
    name = model.StringField()
    region_id = model.ObjectIdField()
    region_type_id = model.ObjectIdField()
    user_id = model.ObjectIdField()
    dashboard_id = model.ObjectIdField()
    ttype = model.IntField(enums=PUBLISH_TTYPE_LIST)

    meta = {
        'indexes': [
            {
                'fields': ['region_type_id'],
            },
            {
                'fields': ['user_id'],
            },
            {
                'fields': ['dashboard_id'],
            },
        ],
    }


NAME_DICT["Publish"] = Publish

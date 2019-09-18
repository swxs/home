# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Publish import *
from ...BaseModel import BaseModelDocument
from settings import instance
from document_utils import NAME_DICT

@instance.register
class Publish(BaseModelDocument):
    name = fields.StringField(allow_none=True)
    region_id = fields.ObjectIdField(allow_none=True)
    region_type_id = fields.ObjectIdField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)
    dashboard_id = fields.ObjectIdField(allow_none=True)
    ttype = fields.IntField(allow_none=True, enums=PUBLISH_TTYPE_LIST)

    class Meta:
        indexes = [
            {
                'key': ['region_type_id'],
            },
            {
                'key': ['user_id'],
            },
            {
                'key': ['dashboard_id'],
            },
        ]
        pass


NAME_DICT["Publish"] = Publish

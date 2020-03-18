# -*- coding: utf-8 -*-
# @File    : Organization.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.Organization import *
from ...BaseModel import BaseModelDocument
from settings import instance


@instance.register
class Organization(BaseModelDocument):
    code = fields.StringField(allow_none=True)
    name = fields.StringField(allow_none=True)
    email = fields.StringField(allow_none=True)
    phone = fields.StringField(allow_none=True)
    status = fields.IntField(allow_none=True, enums=ORGANIZATION_STATUS_LIST, default=ORGANIZATION_STATUS_ACTIVATED)

    class Meta:
        indexes = [
            {
                'key': ['code'],
            },
        ]
        pass

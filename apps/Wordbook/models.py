# -*- coding: utf-8 -*-
# @FILE    : models.py
# @AUTH    : model_creater

import bson
import datetime
from umongo import Instance, Document, fields
from dao.manager.manager_umongo_motor import NAME_DICT
from ..BaseModel import BaseModelDocument
from . import consts
from settings import MONGO_INSTANCE


@MONGO_INSTANCE.register
class Word(BaseModelDocument):
    en = fields.StringField(allow_none=True)
    cn = fields.StringField(allow_none=True)
    number = fields.IntField(allow_none=True, default=0)
    last_time = fields.DateTimeField(allow_none=True)
    user_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        indexes = [
            {
                'key': ['user_id'],
            },
        ]
        pass


NAME_DICT["Word"] = Word

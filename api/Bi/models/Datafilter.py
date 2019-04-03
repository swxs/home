# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine as model
from ..consts.Datafilter import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Datafilter(BaseModelDocument):
    name = model.StringField()
    column_id = model.ObjectIdField()
    worktable_id = model.ObjectIdField()
    dtype = model.IntField(enums=DATAFILTER_DTYPE_LIST)
    custom_attr = model.DictField()


NAME_DICT["Datafilter"] = Datafilter

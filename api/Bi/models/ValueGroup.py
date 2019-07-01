# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ValueGroup import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class ValueGroup(BaseModelDocument):
    name = model.StringField()
    value = model.IntField()
    expression = model.StringField()


NAME_DICT["ValueGroup"] = ValueGroup

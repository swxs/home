# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ValueGroup import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class ValueGroup(BaseModelDocument):
    name = model.StringField(helper_text='分组名称')
    value = model.IntField(helper_text='分组值')
    expression = model.StringField(helper_text='分组表达式')


NAME_DICT["ValueGroup"] = ValueGroup

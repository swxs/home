# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.Tag import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Tag(BaseModelDocument):
    name = model.StringField()
    color = model.StringField()


NAME_DICT["Tag"] = Tag

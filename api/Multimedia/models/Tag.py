# -*- coding: utf-8 -*-
# @File    : Tag.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Tag import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Tag(BaseModelDocument):
    name = model.StringField()
    color = model.StringField()


NAME_DICT["Tag"] = Tag

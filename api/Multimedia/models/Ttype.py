# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.Ttype import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Ttype(BaseModelDocument):
    name = model.StringField()


NAME_DICT["Ttype"] = Ttype

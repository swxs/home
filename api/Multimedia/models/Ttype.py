# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Ttype import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class Ttype(BaseModelDocument):
    name = model.StringField()


NAME_DICT["Ttype"] = Ttype

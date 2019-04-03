# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.Datasource import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Datasource(BaseModelDocument):
    name = model.StringField(helper_text='名称')

    meta = {
        'indexes': [
        ]
    }

NAME_DICT["Datasource"] = Datasource

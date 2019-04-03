# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.Container import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Container(BaseModelDocument):
    name = model.StringField(helper_text='标题')
    show_name = model.BooleanField(default=False, helper_text='是否显示标题')

    meta = {
        'indexes': [
        ]
    }

NAME_DICT["Container"] = Container

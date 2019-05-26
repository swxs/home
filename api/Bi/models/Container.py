# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Container import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class Container(BaseModelDocument):
    name = model.StringField(helper_text='标题')
    show_name = model.BooleanField(default=False, helper_text='是否显示标题')

    meta = {
        'allow_inheritance': True,
    }


NAME_DICT["Container"] = Container

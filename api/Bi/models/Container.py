# -*- coding: utf-8 -*-
# @File    : Container.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Container import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class Container(BaseModelDocument):
    name = model.StringField()
    show_name = model.BooleanField(default=False)

    meta = {
        'allow_inheritance': True,
    }


NAME_DICT["Container"] = Container

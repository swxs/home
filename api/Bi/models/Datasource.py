# -*- coding: utf-8 -*-
# @File    : Datasource.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.Datasource import *
from ...BaseModel import BaseModelDocument
from document_utils import NAME_DICT


class Datasource(BaseModelDocument):
    name = model.StringField()

    meta = {
        'allow_inheritance': True,
    }


NAME_DICT["Datasource"] = Datasource

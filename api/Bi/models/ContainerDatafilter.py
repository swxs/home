# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.ContainerDatafilter import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class ContainerDatafilter(BaseModelDocument):
    data_filter_id = model.ObjectIdField(helper_text='筛选器id')

    meta = {
        'indexes': [
        ]
    }

NAME_DICT["ContainerDatafilter"] = ContainerDatafilter

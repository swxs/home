# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.ContainerGroupDatafilter import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class ContainerGroupDatafilter(BaseModelDocument):
    container_id_list = model.ListField(helper_text='容器id')

    meta = {
        'indexes': [
        ]
    }

NAME_DICT["ContainerGroupDatafilter"] = ContainerGroupDatafilter

# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.ContainerGroup import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class ContainerGroup(BaseModelDocument):
    container_id_list = model.ListField(helper_text='容器id')
    layout_list = model.ListField(helper_text='容器布局信息')

    meta = {
        'indexes': [
        ]
    }

NAME_DICT["ContainerGroup"] = ContainerGroup

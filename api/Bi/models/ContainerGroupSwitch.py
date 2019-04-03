# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.ContainerGroupSwitch import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class ContainerGroupSwitch(BaseModelDocument):
    container_id_list = model.ListField(helper_text='容器id')
    switch_list = model.ListField(helper_text='容器切换条件信息')

    meta = {
        'indexes': [
        ]
    }

NAME_DICT["ContainerGroupSwitch"] = ContainerGroupSwitch

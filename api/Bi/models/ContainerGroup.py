# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ContainerGroup import *
from .Container import Container
from mongoengine_utils import NAME_DICT


class ContainerGroup(Container):
    container_id_list = model.ListField(helper_text='容器id')
    layout_list = model.ListField(helper_text='容器布局信息')

    meta = {
    }


NAME_DICT["ContainerGroup"] = ContainerGroup

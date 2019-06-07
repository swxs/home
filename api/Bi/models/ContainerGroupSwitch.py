# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ContainerGroupSwitch import *
from .Container import Container
from mongoengine_utils import NAME_DICT


class ContainerGroupSwitch(Container):
    container_id_list = model.ListField()
    switch_list = model.ListField()

    meta = {
    }


NAME_DICT["ContainerGroupSwitch"] = ContainerGroupSwitch

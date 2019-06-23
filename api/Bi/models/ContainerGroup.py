# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ContainerGroup import *
from .Container import Container
from document_utils import NAME_DICT


class ContainerGroup(Container):
    container_id_list = model.ListField()
    layout_list = model.ListField()

    meta = {
    }


NAME_DICT["ContainerGroup"] = ContainerGroup

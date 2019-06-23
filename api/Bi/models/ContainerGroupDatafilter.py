# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ContainerGroupDatafilter import *
from .Container import Container
from document_utils import NAME_DICT


class ContainerGroupDatafilter(Container):
    container_id_list = model.ListField()

    meta = {
    }


NAME_DICT["ContainerGroupDatafilter"] = ContainerGroupDatafilter

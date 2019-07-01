# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ContainerDatafilter import *
from .Container import Container
from document_utils import NAME_DICT


class ContainerDatafilter(Container):
    data_filter_id = model.ObjectIdField()

    meta = {
    }


NAME_DICT["ContainerDatafilter"] = ContainerDatafilter

# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ContainerDatafilter import *
from .Container import Container
from mongoengine_utils import NAME_DICT


class ContainerDatafilter(Container):
    data_filter_id = model.ObjectIdField(helper_text='筛选器id')

    meta = {
    }


NAME_DICT["ContainerDatafilter"] = ContainerDatafilter

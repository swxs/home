# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.ContainerDatafilter import *
from .Container import Container
from settings import instance
from document_utils import NAME_DICT

@instance.register
class ContainerDatafilter(Container):
    data_filter_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        pass


NAME_DICT["ContainerDatafilter"] = ContainerDatafilter

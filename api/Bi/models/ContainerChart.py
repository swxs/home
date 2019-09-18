# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model_creater

import datetime
from umongo import Instance, Document, fields
from ..consts.ContainerChart import *
from .Container import Container
from settings import instance
from document_utils import NAME_DICT

@instance.register
class ContainerChart(Container):
    chart_id = fields.ObjectIdField(allow_none=True)

    class Meta:
        pass


NAME_DICT["ContainerChart"] = ContainerChart

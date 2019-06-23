# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ContainerChart import *
from .Container import Container
from document_utils import NAME_DICT


class ContainerChart(Container):
    chart_id = model.ObjectIdField()

    meta = {
    }


NAME_DICT["ContainerChart"] = ContainerChart

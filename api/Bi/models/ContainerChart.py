# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model_creater

import datetime
import mongoengine as model
from ..consts.ContainerChart import *
from .Container import Container
from mongoengine_utils import NAME_DICT


class ContainerChart(Container):
    chart_id = model.ObjectIdField(helper_text='图表id')

    meta = {
    }


NAME_DICT["ContainerChart"] = ContainerChart

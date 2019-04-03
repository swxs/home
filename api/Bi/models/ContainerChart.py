# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model_creater
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine as model
from ..consts.ContainerChart import *
from ...BaseModel import BaseModelDocument
from mongoengine_utils import NAME_DICT


class ContainerChart(BaseModelDocument):
    chart_id = model.ObjectIdField(helper_text='图表id')

    meta = {
        'indexes': [
        ]
    }

NAME_DICT["ContainerChart"] = ContainerChart

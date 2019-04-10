# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.ContainerChart import ContainerChart as _
from .Container import Container
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerChart(Container):
    chart_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(ContainerChart, self).__init__(**kwargs)


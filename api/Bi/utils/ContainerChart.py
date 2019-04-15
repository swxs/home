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

    @property
    def chart(self):
        from .Chart import Chart
        return Chart.get_chart_by_chart_id(self.chart_id)

    @classmethod
    def get_container_chart_by_container_chart_id(cls, container_chart_id):
        return cls.select(id=container_chart_id)


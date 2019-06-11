# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model_creater

from ..dao.ContainerChart import ContainerChart as BaseContainerChart


class ContainerChart(BaseContainerChart):
    def __init__(self, **kwargs):
        super(ContainerChart, self).__init__(**kwargs)

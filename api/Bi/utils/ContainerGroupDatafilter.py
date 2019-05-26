# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model_creater

from ..commons.ContainerGroupDatafilter import ContainerGroupDatafilter as BaseContainerGroupDatafilter


class ContainerGroupDatafilter(BaseContainerGroupDatafilter):
    def __init__(self, **kwargs):
        super(ContainerGroupDatafilter, self).__init__(**kwargs)

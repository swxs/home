# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model_creater

from ..dao.ContainerDatafilter import ContainerDatafilter as BaseContainerDatafilter


class ContainerDatafilter(BaseContainerDatafilter):
    def __init__(self, **kwargs):
        super(ContainerDatafilter, self).__init__(**kwargs)

# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model_creater

from ..dao.ContainerGroupSwitch import ContainerGroupSwitch as BaseContainerGroupSwitch


class ContainerGroupSwitch(BaseContainerGroupSwitch):
    def __init__(self, **kwargs):
        super(ContainerGroupSwitch, self).__init__(**kwargs)

# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model_creater

from ..dao.ContainerGroup import ContainerGroup as BaseContainerGroup


class ContainerGroup(BaseContainerGroup):
    def __init__(self, **kwargs):
        super(ContainerGroup, self).__init__(**kwargs)

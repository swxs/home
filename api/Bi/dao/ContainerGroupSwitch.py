# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.ContainerGroupSwitch import ContainerGroupSwitch as _
from .Container import Container
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerGroupSwitch(Container):
    container_id_list = model.ListField()
    switch_list = model.ListField()

    def __init__(self, **kwargs):
        super(ContainerGroupSwitch, self).__init__(**kwargs)

    @classmethod
    def get_container_group_switch_by_container_group_switch_id(cls, container_group_switch_id):
        return cls.select(id=container_group_switch_id)


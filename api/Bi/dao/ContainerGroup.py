# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.ContainerGroup import ContainerGroup as _
from .Container import Container
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerGroup(Container):
    container_id_list = model.ListField()
    layout_list = model.ListField()

    def __init__(self, **kwargs):
        super(ContainerGroup, self).__init__(**kwargs)

    @classmethod
    async def get_container_group_by_container_group_id(cls, container_group_id):
        return await cls.select(id=container_group_id)


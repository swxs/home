# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.ContainerGroupDatafilter import ContainerGroupDatafilter as _
from .Container import Container
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerGroupDatafilter(Container):
    container_id_list = model.ListField()

    def __init__(self, **kwargs):
        super(ContainerGroupDatafilter, self).__init__(**kwargs)

    @classmethod
    async def get_container_group_datafilter_by_container_group_datafilter_id(cls, container_group_datafilter_id):
        return await cls.select(id=container_group_datafilter_id)


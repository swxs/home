# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.ContainerDatafilter import ContainerDatafilter as _
from .Container import Container
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerDatafilter(Container):
    data_filter_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(ContainerDatafilter, self).__init__(**kwargs)

    @async_property
    async def datafilter(self):
        from .Datafilter import Datafilter
        return await Datafilter.get_datafilter_by_datafilter_id(self.data_filter_id)

    @classmethod
    async def get_container_datafilter_by_container_datafilter_id(cls, container_datafilter_id):
        return await cls.select(id=container_datafilter_id)


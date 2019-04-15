# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.ContainerDatafilter import ContainerDatafilter as _
from .Container import Container
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerDatafilter(Container):
    data_filter_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(ContainerDatafilter, self).__init__(**kwargs)

    @property
    def datafilter(self):
        from .Datafilter import Datafilter
        return Datafilter.get_datafilter_by_datafilter_id(self.data_filter_id)

    @classmethod
    def get_container_datafilter_by_container_datafilter_id(cls, container_datafilter_id):
        return cls.select(id=container_datafilter_id)


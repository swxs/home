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


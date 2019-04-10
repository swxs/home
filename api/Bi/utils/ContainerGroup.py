# -*- coding: utf-8 -*-
# @File    : ContainerGroup.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.ContainerGroup import ContainerGroup as _
from .Container import Container
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerGroup(Container):
    container_id_list = model.ListField()
    layout_list = model.ListField()

    def __init__(self, **kwargs):
        super(ContainerGroup, self).__init__(**kwargs)


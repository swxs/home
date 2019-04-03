# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerGroupDatafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.ContainerGroupDatafilter import ContainerGroupDatafilter as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerGroupDatafilter(BaseUtils):
    container_id_list = model.ListField()

    def __init__(self, **kwargs):
        super(ContainerGroupDatafilter, self).__init__(**kwargs)

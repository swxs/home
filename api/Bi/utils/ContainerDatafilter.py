# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerDatafilter.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.ContainerDatafilter import ContainerDatafilter as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerDatafilter(BaseUtils):
    data_filter_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(ContainerDatafilter, self).__init__(**kwargs)

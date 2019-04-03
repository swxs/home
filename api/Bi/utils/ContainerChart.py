# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerChart.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.ContainerChart import ContainerChart as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerChart(BaseUtils):
    chart_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(ContainerChart, self).__init__(**kwargs)

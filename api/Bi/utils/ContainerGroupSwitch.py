# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : ContainerGroupSwitch.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:19

import datetime
import mongoengine_utils as model
from ..models.ContainerGroupSwitch import ContainerGroupSwitch as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ContainerGroupSwitch(BaseUtils):
    container_id_list = model.ListField()
    switch_list = model.ListField()

    def __init__(self, **kwargs):
        super(ContainerGroupSwitch, self).__init__(**kwargs)

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : DatasourceMerged.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine_utils as model
from ..models.DatasourceMerged import DatasourceMerged as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceMerged(BaseUtils):
    datamerge_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceMerged, self).__init__(**kwargs)

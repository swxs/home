# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : DatasourceRegion.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine_utils as model
from ..models.DatasourceRegion import DatasourceRegion as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class DatasourceRegion(BaseUtils):
    region_type_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(DatasourceRegion, self).__init__(**kwargs)

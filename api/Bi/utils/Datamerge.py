# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine_utils as model
from ..models.Datamerge import Datamerge as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Datamerge(BaseUtils):
    source_worktable_id = model.ObjectIdField()
    source_column_id_list = model.ListField()
    remote_worktable_id = model.ObjectIdField()
    remote_column_id_list = model.ListField()
    how = model.IntField()

    def __init__(self, **kwargs):
        super(Datamerge, self).__init__(**kwargs)

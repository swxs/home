# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

import datetime
import mongoengine_utils as model
from ..models.Worktable import Worktable as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Worktable(BaseUtils):
    name = model.StringField()
    datasource_id = model.ObjectIdField()
    engine = model.IntField()
    status = model.IntField()
    description = model.StringField()

    def __init__(self, **kwargs):
        super(Worktable, self).__init__(**kwargs)

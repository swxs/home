# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model

import datetime
import mongoengine_utils as model
from ..models.Dashboard import Dashboard as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Dashboard(BaseUtils):
    user_id = model.ObjectIdField()
    usage = model.StringField()
    container_id = model.ObjectIdField()
    worktable_id = model.ObjectIdField()
    index = model.IntField()
    name = model.StringField()
    description = model.StringField()
    simulate_region_id = model.ObjectIdField()
    parent_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(Dashboard, self).__init__(**kwargs)

    @classmethod
    def get_dashboard_by_dashboard_id(cls, dashboard_id):
        return cls.select(id=dashboard_id)


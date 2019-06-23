# -*- coding: utf-8 -*-
# @File    : Dashboard.py
# @AUTH    : model_creater

import datetime
import document_utils as model
from ..models.Dashboard import Dashboard as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Dashboard(BaseDAO):
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

    @property
    def container(self):
        from .Container import Container
        return Container.get_container_by_container_id(self.container_id)

    @property
    def worktable(self):
        from .Worktable import Worktable
        return Worktable.get_worktable_by_worktable_id(self.worktable_id)

    @property
    def dashboard(self):
        from .Dashboard import Dashboard
        return Dashboard.get_dashboard_by_dashboard_id(self.parent_id)

    @classmethod
    def get_dashboard_by_dashboard_id(cls, dashboard_id):
        return cls.select(id=dashboard_id)


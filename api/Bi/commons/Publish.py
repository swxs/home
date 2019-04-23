# -*- coding: utf-8 -*-
# @File    : Publish.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Publish import Publish as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Publish(BaseUtils):
    name = model.StringField()
    region_id = model.ObjectIdField()
    region_type_id = model.ObjectIdField()
    user_id = model.ObjectIdField()
    dashboard_id = model.ObjectIdField()
    ttype = model.IntField()

    def __init__(self, **kwargs):
        super(Publish, self).__init__(**kwargs)

    @property
    def dashboard(self):
        from .Dashboard import Dashboard
        return Dashboard.get_dashboard_by_dashboard_id(self.dashboard_id)

    @classmethod
    def get_publish_by_publish_id(cls, publish_id):
        return cls.select(id=publish_id)


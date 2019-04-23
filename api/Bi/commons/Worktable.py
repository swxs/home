# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model_creater

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

    @property
    def datasource(self):
        from .Datasource import Datasource
        return Datasource.get_datasource_by_datasource_id(self.datasource_id)

    @classmethod
    def get_worktable_by_worktable_id(cls, worktable_id):
        return cls.select(id=worktable_id)


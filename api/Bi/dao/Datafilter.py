# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Datafilter import Datafilter as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Datafilter(BaseDAO):
    name = model.StringField()
    column_id = model.ObjectIdField()
    worktable_id = model.ObjectIdField()
    dtype = model.IntField()
    custom_attr = model.DictField()

    def __init__(self, **kwargs):
        super(Datafilter, self).__init__(**kwargs)

    @property
    def column(self):
        from .Column import Column
        return Column.get_column_by_column_id(self.column_id)

    @property
    def worktable(self):
        from .Worktable import Worktable
        return Worktable.get_worktable_by_worktable_id(self.worktable_id)

    @classmethod
    def get_datafilter_by_datafilter_id(cls, datafilter_id):
        return cls.select(id=datafilter_id)

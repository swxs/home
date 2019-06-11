# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.Datamerge import Datamerge as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Datamerge(BaseDAO):
    source_worktable_id = model.ObjectIdField()
    source_column_id_list = model.ListField()
    remote_worktable_id = model.ObjectIdField()
    remote_column_id_list = model.ListField()
    how = model.IntField()

    def __init__(self, **kwargs):
        super(Datamerge, self).__init__(**kwargs)

    @property
    def worktable(self):
        from .Worktable import Worktable
        return Worktable.get_worktable_by_worktable_id(self.source_worktable_id)

    @property
    def worktable(self):
        from .Worktable import Worktable
        return Worktable.get_worktable_by_worktable_id(self.remote_worktable_id)

    @classmethod
    def get_datamerge_by_datamerge_id(cls, datamerge_id):
        return cls.select(id=datamerge_id)


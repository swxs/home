# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.Worktable import Worktable as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Worktable(BaseDAO):
    name = model.StringField()
    datasource_id = model.ObjectIdField()
    engine = model.IntField()
    status = model.IntField()
    description = model.StringField()

    def __init__(self, **kwargs):
        super(Worktable, self).__init__(**kwargs)

    @async_property
    async def datasource(self):
        from .Datasource import Datasource
        return await Datasource.get_datasource_by_datasource_id(self.datasource_id)

    @classmethod
    async def get_worktable_by_worktable_id(cls, worktable_id):
        return await cls.select(id=worktable_id)


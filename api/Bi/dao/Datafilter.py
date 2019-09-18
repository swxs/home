# -*- coding: utf-8 -*-
# @File    : Datafilter.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
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

    @async_property
    async def column(self):
        from .Column import Column
        return await Column.get_column_by_column_id(self.column_id)

    @async_property
    async def worktable(self):
        from .Worktable import Worktable
        return await Worktable.get_worktable_by_worktable_id(self.worktable_id)

    @classmethod
    async def get_datafilter_by_datafilter_id(cls, datafilter_id):
        return await cls.select(id=datafilter_id)


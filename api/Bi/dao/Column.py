# -*- coding: utf-8 -*-
# @File    : Column.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.Column import Column as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class Column(BaseDAO):
    col = model.StringField()
    realcol = model.StringField()
    readablecol = model.StringField()
    worktable_id = model.ObjectIdField()
    is_visible = model.BooleanField()
    is_unique = model.BooleanField()
    dtype = model.IntField()
    ttype = model.IntField()
    expression = model.StringField()
    value_group_id_list = model.StringField()

    def __init__(self, **kwargs):
        super(Column, self).__init__(**kwargs)

    @async_property
    async def worktable(self):
        from .Worktable import Worktable
        return await Worktable.get_worktable_by_worktable_id(self.worktable_id)

    @classmethod
    async def get_column_by_column_id(cls, column_id):
        return await cls.select(id=column_id)


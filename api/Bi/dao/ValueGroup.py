# -*- coding: utf-8 -*-
# @File    : ValueGroup.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.ValueGroup import ValueGroup as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class ValueGroup(BaseDAO):
    name = model.StringField()
    value = model.IntField()
    expression = model.StringField()

    def __init__(self, **kwargs):
        super(ValueGroup, self).__init__(**kwargs)

    @classmethod
    async def get_value_group_by_value_group_id(cls, value_group_id):
        return await cls.select(id=value_group_id)


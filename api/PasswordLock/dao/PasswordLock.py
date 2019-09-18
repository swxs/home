# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from ..models.PasswordLock import PasswordLock as _
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class PasswordLock(BaseDAO):
    name = model.StringField()
    key = model.StringField()
    website = model.StringField()
    user_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)

    @classmethod
    async def get_password_lock_by_password_lock_id(cls, password_lock_id):
        return await cls.select(id=password_lock_id)


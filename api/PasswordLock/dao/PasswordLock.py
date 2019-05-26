# -*- coding: utf-8 -*-
# @File    : PasswordLock.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.PasswordLock import PasswordLock as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class PasswordLock(BaseUtils):
    name = model.StringField()
    key = model.StringField()
    website = model.StringField()
    user_id = model.ObjectIdField()

    def __init__(self, **kwargs):
        super(PasswordLock, self).__init__(**kwargs)

    @classmethod
    def get_password_lock_by_password_lock_id(cls, password_lock_id):
        return cls.select(id=password_lock_id)


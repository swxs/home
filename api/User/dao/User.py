# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

import datetime
import mongoengine_utils as model
from ..models.User import User as _
from ...BaseUtils import BaseUtils
from common.Utils.log_utils import getLogger

log = getLogger("utils/{self.model_name}")


class User(BaseUtils):
    username = model.StringField()
    nickname = model.StringField()
    password = model.StringField()
    salt = model.StringField()
    avatar = model.StringField()
    email = model.StringField()
    mobile = model.StringField()
    description = model.StringField()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @classmethod
    def get_user_by_user_id(cls, user_id):
        return cls.select(id=user_id)


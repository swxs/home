# -*- coding: utf-8 -*-
# @File    : User.py
# @AUTH    : model_creater

import datetime
from async_property import async_property
import document_utils as model
from document_utils.consts import NAME_DICT
from ..models.User import User as UserModel
from ...BaseDAO import BaseDAO
from common.Utils.log_utils import getLogger

log = getLogger("utils/user")


class User(BaseDAO):
    org_id = model.ObjectIdField()
    salt = model.StringField()
    username = model.StringField()
    nickname = model.StringField()
    password = model.StringField()
    phone = model.StringField()
    email = model.StringField()
    avatar = model.StringField()
    description = model.StringField()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @classmethod
    async def get_user_by_user_id(cls, user_id):
        return await cls.select(id=user_id)


NAME_DICT[BaseDAO.__manager__]["User"] = UserModel
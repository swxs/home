# -*- coding: utf-8 -*-
# @FILE    : utils/user_auth.py
# @AUTH    : model_creater

from ..dao.user_auth import UserAuth
from ..dao.user import User


def pre_create(params):
    if params.get("user_id") is None:
        user = User.create()
    params["user_id"] = user.id
    return params


UserAuth.pre_create = pre_create

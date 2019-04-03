# -*- coding: utf-8 -*-
# @File    : BaseUtils.py
# @AUTH    : swxs
# @Time    : 2019/4/3 10:26

import datetime
import mongoengine_utils as model


class BaseUtils(model.BaseDocument):
    created = model.DateTimeField()
    updated = model.DateTimeField(pre_update=datetime.datetime.now)

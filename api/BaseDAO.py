# -*- coding: utf-8 -*-
# @File    : BaseDAO.py
# @AUTH    : swxs
# @Time    : 2019/4/3 10:26

import datetime
import document_utils as model


class BaseDAO(model.BaseDocument):
    __manager__ = "umongo_motor"

    created = model.DateTimeField(create=False)
    updated = model.DateTimeField(create=False, pre_update=datetime.datetime.now)

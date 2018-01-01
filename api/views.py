# -*- coding: utf-8 -*-
'''
@author: xuyi
@created: 2016-12-14 17:46:18
@description:
@updated: 2016-12-14 17:46:18
'''
import datetime
import re
import tornado

from base import BaseHandler


class IndexHandler(BaseHandler):
    @BaseHandler.ajax_base
    def get(self):
        return []

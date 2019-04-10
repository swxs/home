# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Worktable import Worktable

log = getLogger("views/Worktable")


class WorktableHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, worktable_id=None):
        if worktable_id:
            worktable = Worktable.select(id=worktable_id)
            return worktable.to_front()
        else:
            worktable_list = Worktable.filter()
            return [worktable.to_front() for worktable in worktable_list]

    @BaseHandler.ajax_base()
    def post(self, worktable_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['datasource_id'] = self.get_argument('datasource_id', None)
        params['engine'] = self.get_argument('engine', None)
        params['status'] = self.get_argument('status', None)
        params['description'] = self.get_argument('description', None)
        worktable = Worktable.create(**params)
        return worktable.id

    @BaseHandler.ajax_base()
    def put(self, worktable_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['datasource_id'] = self.get_argument('datasource_id', None)
        params['engine'] = self.get_argument('engine', None)
        params['status'] = self.get_argument('status', None)
        params['description'] = self.get_argument('description', None)
        worktable = Worktable.select(id=worktable_id)
        worktable = worktable.update(**params)
        return worktable.id

    @BaseHandler.ajax_base()
    def patch(self, worktable_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['datasource_id'] = self.get_argument('datasource_id', undefined)
        params['engine'] = self.get_argument('engine', undefined)
        params['status'] = self.get_argument('status', undefined)
        params['description'] = self.get_argument('description', undefined)
        worktable = Worktable.select(id=worktable_id)
        worktable = worktable.update(**params)
        return worktable.id

    @BaseHandler.ajax_base()
    def delete(self, worktable_id=None):
        worktable = Worktable.select(id=worktable_id)
        worktable.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")

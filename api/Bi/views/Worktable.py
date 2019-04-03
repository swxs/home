# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
# @File    : Worktable.py
# @AUTH    : model
# @Time    : 2019-04-03 15:07:20

from base import BaseHandler
from api.consts.const import undefined
from ..utils.Worktable import Worktable
from common.Utils.log_utils import getLogger

log = getLogger("views/Worktable")


class WorktableHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, worktable_id=None):
        if worktable_id:
            worktable = Worktable.select(id=worktable_id)
            return Worktable.to_front()
        else:
            worktable_list = Worktable.filter()
            return [worktable.to_front() for worktable in worktable_list]

    @BaseHandler.ajax_base()
    def post(self):
        params = self.get_all_arguments()
        worktable = Worktable.create(params)
        return worktable.to_front()

    @BaseHandler.ajax_base()
    def put(self, worktable_id):
        params = self.get_all_arguments()
        worktable = Worktable.select(id=worktable_id)
        worktable = worktable.update(params)
        return worktable.to_front()

    @BaseHandler.ajax_base()
    def patch(self, worktable_id):
        params = self.get_all_arguments()
        worktable = Worktable.select(id=worktable_id)
        worktable = worktable.update(params)
        return worktable.to_front()

    @BaseHandler.ajax_base()
    def delete(self, worktable_id):
        worktable = Worktable.select(id=worktable_id)
        worktable.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")

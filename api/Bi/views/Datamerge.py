# -*- coding: utf-8 -*-
# @File    : Datamerge.py
# @AUTH    : model

from base import BaseHandler
from common.Utils.log_utils import getLogger
from ...BaseConsts import *
from ..utils.Datamerge import Datamerge

log = getLogger("views/Datamerge")


class DatamergeHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, datamerge_id=None):
        if datamerge_id:
            datamerge = Datamerge.select(id=datamerge_id)
            return datamerge.to_front()
        else:
            datamerge_list = Datamerge.filter()
            return [datamerge.to_front() for datamerge in datamerge_list]

    @BaseHandler.ajax_base()
    def post(self, datamerge_id=None):
        if datamerge_id:
            params = dict()
            params['source_worktable_id'] = self.get_argument('source_worktable_id', undefined)
            params['source_column_id_list'] = self.get_arguments('source_column_id_list', undefined)
            params['remote_worktable_id'] = self.get_argument('remote_worktable_id', undefined)
            params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', undefined)
            params['how'] = self.get_argument('how', undefined)
            datamerge = Datamerge.select(id=datamerge_id)
            datamerge = datamerge.copy(**params)
            return datamerge.id
        else:
            params = dict()
            params['source_worktable_id'] = self.get_argument('source_worktable_id', None)
            params['source_column_id_list'] = self.get_arguments('source_column_id_list', [])
            params['remote_worktable_id'] = self.get_argument('remote_worktable_id', None)
            params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', [])
            params['how'] = self.get_argument('how', None)
            datamerge = Datamerge.create(**params)
            return datamerge.id

    @BaseHandler.ajax_base()
    def put(self, datamerge_id=None):
        params = dict()
        params['source_worktable_id'] = self.get_argument('source_worktable_id', None)
        params['source_column_id_list'] = self.get_arguments('source_column_id_list', [])
        params['remote_worktable_id'] = self.get_argument('remote_worktable_id', None)
        params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', [])
        params['how'] = self.get_argument('how', None)
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge = datamerge.update(**params)
        return datamerge.id

    @BaseHandler.ajax_base()
    def patch(self, datamerge_id=None):
        params = dict()
        params['source_worktable_id'] = self.get_argument('source_worktable_id', undefined)
        params['source_column_id_list'] = self.get_arguments('source_column_id_list', undefined)
        params['remote_worktable_id'] = self.get_argument('remote_worktable_id', undefined)
        params['remote_column_id_list'] = self.get_arguments('remote_column_id_list', undefined)
        params['how'] = self.get_argument('how', undefined)
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge = datamerge.update(**params)
        return datamerge.id

    @BaseHandler.ajax_base()
    def delete(self, datamerge_id=None):
        datamerge = Datamerge.select(id=datamerge_id)
        datamerge.delete()
        return None

    def set_default_headers(self):
        self._headers.add("version", "1")

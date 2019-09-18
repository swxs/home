# -*- coding: utf-8 -*-
# @File    : Ttype.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.Ttype import Ttype

log = getLogger("views/Ttype")


class TtypeHandler(BaseHandler):
    @BaseHandler.ajax_base()
    def get(self, ttype_id=None):
        if ttype_id:
            ttype = Ttype.select(id=ttype_id)
            return SuccessData(
                ttype.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            ttype_cursor = Ttype.search(**search_params)
            data = []
            for ttype in ttype_cursor:
                data.append(ttype.to_front())
            return SuccessData(data)
            # pager = Page(ttype_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    def post(self, ttype_id=None):
        if ttype_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            ttype = Ttype.select(id=ttype_id)
            ttype = ttype.copy(**params)
            return SuccessData(
                ttype.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            ttype = Ttype.create(**params)
            return SuccessData(
                ttype.id
            )

    @BaseHandler.ajax_base()
    def put(self, ttype_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        ttype = Ttype.select(id=ttype_id)
        ttype = ttype.update(**params)
        return SuccessData(
            ttype.id
        )

    @BaseHandler.ajax_base()
    def patch(self, ttype_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        ttype = Ttype.select(id=ttype_id)
        ttype = ttype.update(**params)
        return SuccessData(
            ttype.id
        )

    @BaseHandler.ajax_base()
    def delete(self, ttype_id=None):
        ttype = Ttype.select(id=ttype_id)
        ttype.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")

# -*- coding: utf-8 -*-
# @File    : Organization.py
# @AUTH    : model

import json
from tornado.web import url
from web.web import BaseHandler
from web.consts import undefined
from web.result import SuccessData
from web.decorator.render import render
from common.Helpers.Helper_pagenate import Page
from common.Utils.log_utils import getLogger
from ..utils.Organization import Organization, organization_schema

log = getLogger("views/organization")


class OrganizationHandler(BaseHandler):
    @render
    async def get(self, organization_id=None):
        if organization_id:
            organization = await Organization.select(id=organization_id)
            return SuccessData(
                data=await organization.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            order_by = self.get_argument("order_by", "")
            use_pager = int(self.get_argument("use_pager", 1))
            page = int(self.get_argument("page", 1))
            items_per_page = int(self.get_argument("items_per_page", 20))

            item_count = await Organization.count(**search_params)
            if use_pager:
                search_params.update({
                    "limit": items_per_page,
                    "skip": (page - 1) * items_per_page
                })
            order_by = [o for o in order_by.split(";") if bool(o)]
            organization_cursor = Organization.search(**search_params).order_by(order_by)
            data = [await  organization.to_front() async for organization in organization_cursor]
            pager = Page(data, use_pager=use_pager, page=page, items_per_page=items_per_page, item_count=item_count)
            return SuccessData(
                data=pager.items, 
                info=pager.info
            )


    @render
    async def post(self, organization_id=None):
        if organization_id:
            params = organization_schema.load(self.arguments, partial=True)
            old_organization = await Organization.select(id=organization_id)
            new_organization = await old_organization.copy(**params.data)
            return SuccessData(
                id=new_organization.id
            )
        else:
            params = organization_schema.load(self.arguments)
            organization = await Organization.create(**params.data)
            return SuccessData(
                id=organization.id
            )

    @render
    async def put(self, organization_id=None):
        params = organization_schema.load(self.arguments)
        organization = await Organization.find_and_update(id=organization_id, **params.data)
        return SuccessData(
            id=organization.id
        )

    @render
    async def patch(self, organization_id=None):
        params = organization_schema.load(self.arguments, partial=True)
        organization = await Organization.find_and_update(id=organization_id, **params.data)
        return SuccessData(
            id=organization.id
        )

    @render
    async def delete(self, organization_id=None):
        count = await Organization.find_and_delete(id=organization_id)
        return SuccessData(
            count=count
        )

    def set_default_headers(self):
        self._headers.add("version", "1")


URL_MAPPING_LIST = [
    url(r"/api/system/organization/(?:([a-zA-Z0-9&%\.~-]+)/)?", OrganizationHandler),
]

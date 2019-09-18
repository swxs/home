# -*- coding: utf-8 -*-
# @File    : DatasourceSurvey.py
# @AUTH    : model

import json
from bson import ObjectId
from common.Utils.log_utils import getLogger
from common.Helpers.Helper_pagenate import Page
from ...BaseConsts import *
from ...BaseViews import BaseHandler, SuccessData
from ..utils.DatasourceSurvey import DatasourceSurvey

log = getLogger("views/DatasourceSurvey")


class DatasourceSurveyHandler(BaseHandler):
    @BaseHandler.ajax_base()
    async def get(self, datasource_survey_id=None):
        if datasource_survey_id:
            datasource_survey = await DatasourceSurvey.select(id=datasource_survey_id)
            return SuccessData(
                await datasource_survey.to_front()
            )
        else:
            search_params = json.loads(self.get_argument("search", '{}'))
            use_pager = self.get_argument("use_pager", 1)
            page = self.get_argument("page", 1)
            items_per_page = self.get_argument("items_per_page", 20)
            datasource_survey_cursor = DatasourceSurvey.search(**search_params)
            data = []
            async for datasource_survey in datasource_survey_cursor:
                data.append(await datasource_survey.to_front())
            return SuccessData(data)
            # pager = Page(datasource_survey_list, use_pager=use_pager, page=page, items_per_page=items_per_page)
            # return SuccessData(
            #     [await item.to_front() for item in pager.items],
            #     info=pager.info,
            # )

    @BaseHandler.ajax_base()
    async def post(self, datasource_survey_id=None):
        if datasource_survey_id:
            params = dict()
            params['name'] = self.get_argument('name', undefined)
            params['survey_id'] = self.get_argument('survey_id', undefined)
            datasource_survey = await DatasourceSurvey.select(id=datasource_survey_id)
            datasource_survey = await datasource_survey.copy(**params)
            return SuccessData(
                datasource_survey.id
            )
        else:
            params = dict()
            params['name'] = self.get_argument('name', None)
            params['survey_id'] = self.get_argument('survey_id', None)
            datasource_survey = await DatasourceSurvey.create(**params)
            return SuccessData(
                datasource_survey.id
            )

    @BaseHandler.ajax_base()
    async def put(self, datasource_survey_id=None):
        params = dict()
        params['name'] = self.get_argument('name', None)
        params['survey_id'] = self.get_argument('survey_id', None)
        datasource_survey = await DatasourceSurvey.select(id=datasource_survey_id)
        datasource_survey = await datasource_survey.update(**params)
        return SuccessData(
            datasource_survey.id
        )

    @BaseHandler.ajax_base()
    async def patch(self, datasource_survey_id=None):
        params = dict()
        params['name'] = self.get_argument('name', undefined)
        params['survey_id'] = self.get_argument('survey_id', undefined)
        datasource_survey = await DatasourceSurvey.select(id=datasource_survey_id)
        datasource_survey = await datasource_survey.update(**params)
        return SuccessData(
            datasource_survey.id
        )

    @BaseHandler.ajax_base()
    async def delete(self, datasource_survey_id=None):
        datasource_survey = await DatasourceSurvey.select(id=datasource_survey_id)
        await datasource_survey.delete()
        return SuccessData(
            None
        )

    def set_default_headers(self):
        self._headers.add("version", "1")

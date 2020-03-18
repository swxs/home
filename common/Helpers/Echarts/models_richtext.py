# -*- coding: utf-8 -*-
# @File    : models_richtext.py
# @AUTH    : swxs
# @Time    : 2019/6/17 15:39

from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype
from apps.bi import model_enums

logger = log_utils.get_logging(name='model', file_name='model.log')


class RichtextChart(BaseChart):
    name = model_enums.CHART_TTYPE_RICHTEXT

    def __init__(self, dbchart, dh, **params):
        super().__init__(dbchart, dh, **params)
        self.chart_option.update(dict(
            show_type="richtext"
        ))

    async def to_option(self):
        return self.dbchart.custom_attr.get("richtext", ""), self.chart_option

    async def to_export_data(self):
        return None

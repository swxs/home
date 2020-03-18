# coding=utf8
import math
from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype
from apps.bi import model_enums
from apps.bi import chart_enums
from apps.bi import field_utils

logger = log_utils.get_logging(name='model', file_name='model.log')


class CustomMadeChart(BaseChart):
    name = model_enums.CHART_TTYPE_CUSTOM_MADE

    def __init__(self, dbchart, dh, **params):
        super().__init__(dbchart, dh, **params)
        self.chart_option.update(dict(
            show_type="custom"
        ))

    async def to_option(self):
        return {}, self.chart_option

    async def to_export_data(self):
        return None

# coding=utf8

from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class TreeMapChart(BaseChart):
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        pass

    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        return super(TreeMapChart, self).to_export_data()

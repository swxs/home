# coding=utf8

from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class ScatterChart(BaseChart):
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        self.get_base_chart_option()
        
        serie = None
        self.option.series = []
        
        if not (self.dbchart.datax and self.dbchart.datay):
            return self.option
        serie_option_list, chart_option = self.get_scatter_serie_option()
        self.option.series.extend(serie_option_list)
        
        if serie and hasattr(serie, 'pd_serie'):
            self.pd_serie = serie.pd_serie
        
        self.set_option_title()
        self.set_option_legend()
        return self.option, chart_option
    
    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        return super(ScatterChart, self).to_export_data()

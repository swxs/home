# coding=utf8

from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class HbarChart(BaseChart):
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        self.get_base_chart_option()
        self.set_option_y_grid_type()
        self.chart_option = dict()
        
        try:
            self.get_filtered_df()
        except NoDataException:
            return self.option, {}
        
        self.get_index()
        if not self.get_pivot_df():
            return self.option, {}
        self.get_ranked_df()
        self.get_series_list()

        self.set_color()
        self.set_option_legend_icon(ttype="circle")
        self.set_option_colorset()
        self.set_option_visualmap()
        self.set_option_title()
        self.set_option_legend()
        self.set_option_toolbox()
        self.set_option_axis_title()
        self.set_option_xaxis_auto_change()
        self.set_option_yaxis_data(self.axis_data_list)
        self.set_option_yaxis_hidden()
        self.set_option_yaxis_rotate()
        self.set_option_datazoom()
        self.set_option_xaxis_formatter()
        self.set_option_series_formatter()
        self.set_markline()
        
        self.chart_option.update(dict(
            drilldown_info=self._get_drilldown_info(),
            formatterDict=self.formatterDict
        ))
        
        return self.option, self.chart_option
    
    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        return super(HbarChart, self).to_export_data()

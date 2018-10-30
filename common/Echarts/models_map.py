# coding=utf8

from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class MapChart(BaseChart):
    def get_series_list(self):
        result = self.dh.get_pivot_data_result()
        self.legend_data_list = []
        series_list = []
        for data in result["data"]:
            series_option = self.get_base_series_option()
            series_option.name = self._convert_field_name(result["head"]["name"][0])
            for i, value in enumerate(data["value"]):
                series_option.data.append(dict(name=self._convert_column_name(result["head"]["value"][i], field_list=result["head"]["name"]), value=self._clear_data(value)))
            series_option.field_id = data["name"]
            series_option.id = data["name"]
            series_list.append(series_option)
            self.legend_data_list.append(series_option.name)
        self.option.series = series_list
        self.option.legend.data = self.legend_data_list
    
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        self.get_base_chart_option()
        self.chart_option = dict()
        
        try:
            self.get_filtered_df()
        except NoDataException:
            return self.option, {}
        
        self.get_index()
        if not self.get_pivot_df():
            return self.option, {}
        self.get_series_list()

        self.set_color()
        self.set_option_colorset()
        self.set_option_visualmap()
        self.set_option_title()
        self.set_option_legend()
        self.set_option_toolbox()
        self.set_option_series_formatter()
        
        self.chart_option.update(dict(
            drilldown_info=self._get_drilldown_info(),
            formatterDict=self.formatterDict
        ))
        
        return self.option, self.chart_option
    
    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        return super(MapChart, self).to_export_data()

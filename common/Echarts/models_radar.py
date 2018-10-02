# coding=utf8

from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class RadarChart(BaseChart):
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        self.get_base_chart_option()
        try:
            self.get_filtered_df()
        except NoDataException:
            return self.option, {}
        self.get_index()
        if not self.get_pivot_df():
            return self.option, {}
        self.get_ranked_df()
        series_list = []
        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_N_COLOR_Y_INDEX,
                          Vtype.N_VALUE_Y_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX]:
            return self.option, {}
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_Y_COLOR_N_INDEX]:
            result = self.dh.get_pivot_data_result()
            self.radar_indicator_list = [self._convert_field_name(data.get('name')) for data in result["data"]]
            self.legend_data_list = result["head"]["name"]
            series_option = self.get_base_series_option()
            data_list = [self._convert_field_name(data.get('data')) for data in result["data"]]
            series_option.data.append(data_list)
            series_option.name = "All"
            series_list.append(series_option)
            self.option.series = series_list
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_Y_INDEX, Vtype.Y_VALUE_Y_COLOR_Y_INDEX]:
            result = self.dh.get_pivot_data_result()
            self.radar_indicator_list = [self._convert_column_name(value, field_list=result["head"]["name"])
                                         for value in result["head"]["value"]]
            self.legend_data_list = []
            for data in result["data"]:
                series_option = self.get_base_series_option()
                series_option.data = [self._convert_name(value) for value in data["value"]]
                series_option.name = self._convert_field_name(data["name"])
                self.legend_data_list.append(series_option.name)
                series_list.append(series_option)
            self.option.series = series_list
        for indicator in self.radar_indicator_list:
            self.option.radar.indicator.append({"name": indicator})

        self.set_color()
        self.set_option_legend_icon(ttype="circle")
        self.set_option_title()
        self.set_option_legend()
        self.set_option_toolbox()
        return self.option, {}

    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        return super(RadarChart, self).to_export_data()

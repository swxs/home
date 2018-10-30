# coding=utf8

from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class GaugeChart(BaseChart):
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        self.get_base_chart_option()
        self.chart_option = dict()
        
        try:
            self.get_filtered_df()
        except NoDataException:
            return self.option, {}
        
        self.get_index()
        
        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_N_INDEX,
                          Vtype.Y_VALUE_Y_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX,
                          Vtype.Y_VALUE_Y_COLOR_Y_INDEX, Vtype.N_VALUE_N_COLOR_Y_INDEX]:
            return self.option, self.chart_option
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_N_COLOR_Y_INDEX]:
            self.get_df()
            series_list = []
            result = self.dh.get_pivot_data_result()
            for i, head_value in enumerate(result["head"]["value"]):
                series_option = self.get_base_series_option()
                for data in result["data"]:
                    if len(data["value"]) > 0:
                        series_option.data.append({'name': self._convert_field_name(data["name"]), 'value': self._clear_data(data["value"][i])})
                    else:
                        series_option.data.append({'name': self._convert_field_name(data["name"]), 'value': self._clear_data(i)})
                    series_option.field_id = data["name"]
                    series_option.id = data["name"]
                series_option.name = self._convert_column_name(result["head"]["value"][i], field_list=result["head"]["name"])
                series_list.append(series_option)
        
        self.option.series = series_list
        
        def_max_value = 100
        def_min_value = 0
        
        if len(self.option.series) > 0:
            def_value = self.option.series[0].data[0]["value"]
            if def_value == "-":
                def_value = 0
            def_max_value = round(def_value * 2)
            def_min_value = 0
            if self.dbchart.custom_attr is not None:
                if "gauge_range" in self.dbchart.custom_attr:
                    if self.dbchart.custom_attr["gauge_range"]:
                        def_max_value = self.dbchart.custom_attr.get("gauge_range_max", def_max_value)
                        def_min_value = self.dbchart.custom_attr.get("gauge_range_min", 0)
            self.option.series[0]['max'] = def_max_value
            self.option.series[0]['min'] = def_min_value
        
        self.set_option_series_formatter()
        self.chart_option.update(dict(
            max=def_max_value,
            min=def_min_value,
            formatterDict=self.formatterDict
        ))
        return self.option, self.chart_option
    
    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        return super(GaugeChart, self).to_export_data()

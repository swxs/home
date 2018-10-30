# coding=utf8

from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class PieChart(BaseChart):
    def set_option_series_formatter(self):
        formatter_kwargs = self._get_formatter_dict(self.dbchart, key="default_field_formatter")
        self.option["tooltip"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)
        formatter_kwargs.update(dict(showAxis=False))
        for series in self.option.series:
            series["label"]["normal"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)
        formatter_kwargs.update(dict(showText=True, showAxis=True))
        for series in self.option.series:
            series["tooltip"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)

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
        self.get_ranked_df()
        series_list = []
        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_N_COLOR_Y_INDEX,
                          Vtype.N_VALUE_Y_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX]:
            return self.option, {}
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_Y_COLOR_N_INDEX]:
            result = self.dh.get_pivot_data_result()
            self.legend_data_list = [self._convert_field_name(x["name"]) for x in result["data"]]
            series_option = self.get_base_series_option()
            series_option.name = result["head"]["name"][0]
            for data in result["data"]:
                series_option.data.append({"name": self._convert_field_name(data["name"]), "value": self._clear_data(data["value"][0])})
            series_list.append(series_option)
            self.option.series = series_list
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_Y_INDEX, Vtype.Y_VALUE_Y_COLOR_Y_INDEX]:
            result = self.dh.get_pivot_data_result()
            self.legend_data_list = [self._convert_column_name(x, field_list=result["head"]["name"])
                                     for x in result["head"]["value"]]
            for data in result["data"]:
                series_option = self.get_base_series_option()
                series_option.name = self._convert_field_name(data["name"])
                for i, data in enumerate(data["value"]):
                    series_option.data.append({"name": self.legend_data_list[i], "value": self._clear_data(data)})
                series_list.append(series_option)
            self.option.series = series_list

        self.set_color()
        self.set_option_legend_icon(ttype="circle")
        self.set_option_radius()
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
        return super(PieChart, self).to_export_data()

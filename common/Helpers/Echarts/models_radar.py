# coding=utf8
from apps.errors import AppResourceError
from exceptions import ResourceError
from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype
from apps.bi import model_enums

logger = log_utils.get_logging(name='model', file_name='model.log')


class RadarChart(BaseChart):
    name = model_enums.CHART_TTYPE_RADAR

    @BaseChart.delete_df_already_used_column
    async def to_option(self):
        await self.create(self.dbchart)

        self.get_base_chart_option()
        try:
            await self.get_filtered_df()
        except ResourceError as e:
            return self.option, self.chart_option

        await self.get_index()
        if not await self.get_pivot_df():
            return self.option, self.chart_option
        await self.get_ranked_df()
        series_list = []
        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_N_COLOR_Y_INDEX,
                          Vtype.N_VALUE_Y_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX]:
            return self.option, self.chart_option
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_Y_COLOR_N_INDEX]:
            result = self.dh.get_pivot_data_result()
            self.radar_indicator_list = [await self._convert_field_name(data.get('name')) for data in result["data"]]
            self.legend_data_list = result["head"]["name"]
            series_option = self.get_base_series_option()
            series_option.data = []
            data_list = [await self._convert_field_name(data.get('data')) for data in result["data"]]
            series_option.data.append(data_list)
            series_option.name = ""
            series_list.append(series_option)
            self.option.series = series_list
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_Y_INDEX, Vtype.Y_VALUE_Y_COLOR_Y_INDEX]:
            result = self.dh.get_pivot_data_result()
            self.radar_indicator_list = [
                await self._convert_column_value(value, field_list=result["head"]["name"])
                for value in result["head"]["value"]
            ]
            self.legend_data_list = []
            for data in result["data"]:
                series_option = self.get_base_series_option()
                series_option.data = [self._convert_string_value(value) for value in data["value"]]
                series_option.name = await self._convert_field_name(data["name"])
                self.legend_data_list.append(series_option.name)
                series_list.append(series_option)
            self.option.series = series_list
        for indicator in self.radar_indicator_list:
            self.option.radar.indicator.append({"name": indicator})

        await self.set_option_color()
        await self.set_option_title()
        await self.set_option_toolbox()
        await self.set_option_legend(icon="circle")

        return self.option, {}

    @BaseChart.delete_df_already_used_column
    async def to_export_data(self):
        return await super(RadarChart, self).to_export_data()

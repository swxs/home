# coding=utf8

from apps.errors import AppResourceError
from exceptions import ResourceError
from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype
from apps.bi import model_enums

logger = log_utils.get_logging(name='model', file_name='model.log')


class MapChart(BaseChart):
    name = model_enums.CHART_TTYPE_MAP

    def hook_visual_map_kwargs(self, visual_map_kwargs):
        visual_map_kwargs.update(dict(dimension=0))

    async def get_series_list(self):
        result = self.dh.get_pivot_data_result()
        self.legend_data_list = []
        series_list = []
        for data in result["data"]:
            series_option = self.get_base_series_option()
            series_option.data = []
            series_option.name = await self._convert_field_name(result["head"]["name"][0])
            for i, value in enumerate(data["value"]):
                series_option.data.append(dict(name=await self._convert_column_value(result["head"]["value"][i], field_list=result["head"]["name"]), value=self._convert_number_value(value)))
            series_option.field_id = data["name"]
            series_option.id = data["name"]
            series_list.append(series_option)
            self.legend_data_list.append(series_option.name)
        self.option.series = series_list
        self.option.legend.data = self.legend_data_list

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
            return self.option, {}
        await self.get_series_list()

        await self.set_option_color()
        await self.set_option_title()
        await self.set_option_toolbox()
        await self.set_option_legend()
        await self.set_option_series_formatter()

        self.chart_option.update(dict(
            drill_down_info=await self._get_drilldown_info(),
            formatterDict=self.formatterDict
        ))

        return self.option, self.chart_option

    @BaseChart.delete_df_already_used_column
    async def to_export_data(self):
        return await super(MapChart, self).to_export_data()

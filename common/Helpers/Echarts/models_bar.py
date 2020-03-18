# coding=utf8

from apps.bi import model_enums
from apps.errors import AppResourceError
from exceptions import ResourceError
from commons import log_utils
from commons.Echarts.models_base import BaseChart

logger = log_utils.get_logging(name='model', file_name='model.log')


class BarChart(BaseChart):
    name = model_enums.CHART_TTYPE_BAR

    async def _get_series_index(self, line_field, type_line_data):
        type_line_data.update(yAxis=type_line_data["axis"])
        return await super(BarChart, self)._get_series_index(line_field, type_line_data)

    @BaseChart.delete_df_already_used_column
    async def to_option(self):
        await self.create(self.dbchart)

        self.get_base_chart_option()
        self.set_option_x_grid_type()

        try:
            await self.get_filtered_df()
        except ResourceError as e:
            return self.option, self.chart_option

        await self.get_index()
        if not await self.get_pivot_df():
            return self.option, self.chart_option
        await self.get_ranked_df()
        await self.get_series_list()

        await self.set_option_color()
        await self.set_option_title()
        await self.set_option_toolbox()
        await self.set_option_legend(icon="circle")
        await self.set_option_x_axis(data=self.axis_data_list)
        await self.set_option_y_axis(format=True, show_line=False)
        await self.set_option_data_zoom()
        await self.set_option_series_formatter()
        await self.set_option_mark_line()

        self.chart_option.update(dict(
            drill_down_info=await self._get_drilldown_info(),
            formatterDict=self.formatterDict
        ))

        return self.option, self.chart_option

    @BaseChart.delete_df_already_used_column
    async def to_export_data(self):
        return await super(BarChart, self).to_export_data()

# coding=utf8
from apps.errors import AppResourceError
from exceptions import ResourceError
from apps.bi import model_enums
from apps.bi import chart_enums
from apps.bi import field_utils
from commons import consts
from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype

logger = log_utils.get_logging(name='model', file_name='model.log')


class PieChart(BaseChart):
    async def set_option_value_visualmap_color(self):
        def _get_text_value(value, base=0):
            return int(value) + base

        for i, series in enumerate(self.option.series):
            for j, data in enumerate(series.data):
                field_id = self._get_series_field(data)
                if field_id is None:
                    continue
                if not self._has_visual_map(field_id):
                    continue
                field = await field_utils.get_field(field_id)
                advanced_color_type = field.custom_attr.get('advanced_color_type', None)
                if (not advanced_color_type) or advanced_color_type == chart_enums.CHART_VMTYPE_NORMAL:
                    if field.custom_attr.get('color', None):
                        data["itemStyle"] = {
                            "normal": {
                                "color": field.custom_attr.get('color', None)
                            }
                        }

    async def set_option_color(self):
        if self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_INDEX:
            await self.set_option_color_set()
        elif self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_VALUE:
            await self.set_option_color_set()
            await self.set_option_value_visualmap_color()
        else:
            await self.set_option_color_set()

    name = model_enums.CHART_TTYPE_PIE

    async def set_option_series_formatter(self):
        formatter_kwargs = self._get_formatter_dict(
            self.dbchart, 
            key="default_value_field_formatter", 
            default_show_text=True, 
            default_show_value=False
        )

        self.hook_tooltip_formatter(formatter_kwargs)
        self.option["tooltip"]["formatter"] = self._get_formatter_funcstr(default_show_text=True, default_show_value=False, **formatter_kwargs)

        for series in self.option.series:
            self.hook_label_formatter(formatter_kwargs)
            series["label"]["normal"]["formatter"] = self._get_formatter_funcstr(default_show_text=True, default_show_value=False, **formatter_kwargs)

        for series in self.option.series:
            self.hook_tooltip_formatter(formatter_kwargs)
            series["tooltip"]["formatter"] = self._get_formatter_funcstr(default_show_text=True, default_show_value=False, **formatter_kwargs)

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
        if self.vtype in [
            Vtype.N_VALUE_N_COLOR_N_INDEX,
            Vtype.N_VALUE_N_COLOR_Y_INDEX,
            Vtype.N_VALUE_Y_COLOR_N_INDEX,
            Vtype.N_VALUE_Y_COLOR_Y_INDEX,
            Vtype.Y_VALUE_Y_COLOR_N_INDEX,
            Vtype.Y_VALUE_Y_COLOR_Y_INDEX,
        ]:
            return self.option, self.chart_option
        elif self.vtype in [
            Vtype.Y_VALUE_N_COLOR_N_INDEX,
        ]:
            result = self.dh.get_pivot_data_result()
            self.legend_data_list = [await self._convert_field_name(x["name"]) for x in result["data"]]
            series_option = self.get_base_series_option()
            series_option.data = []
            series_option.name = result["head"]["name"][0]
            for data in result["data"]:
                series_option.data.append({
                    "name": await self._convert_field_name(data["name"]),
                    "value": self._convert_number_value(data["value"][0]),
                    "field_id": data["name"],
                })
            series_list.append(series_option)
            self.option.series = series_list
        elif self.vtype in [
            Vtype.Y_VALUE_N_COLOR_Y_INDEX,
        ]:
            result = self.dh.get_pivot_data_result()
            self.legend_data_list = [
                await self._convert_column_value(x, field_list=result["head"]["name"])
                for x in result["head"]["value"]
            ]
            for data in result["data"]:
                series_option = self.get_base_series_option()
                series_option.data = []
                series_option.name = await self._convert_field_name(data["name"])
                for i, data in enumerate(data["value"]):
                    series_option.data.append(
                        {
                            "name": self.legend_data_list[i],
                            "value": self._convert_number_value(data)
                        }
                    )
                series_list.append(series_option)
            self.option.series = series_list

        await self.set_option_color()
        await self.set_option_title()
        await self.set_option_toolbox()
        await self.set_option_legend(icon="circle")
        await self.set_option_radius()
        await self.set_option_series_formatter()

        self.chart_option.update(dict(
            drill_down_info=await self._get_drilldown_info(),
            formatterDict=self.formatterDict
        ))

        return self.option, self.chart_option

    @BaseChart.delete_df_already_used_column
    async def to_export_data(self):
        return await super(PieChart, self).to_export_data()

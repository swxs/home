# coding=utf8
from apps.errors import AppResourceError
from exceptions import ResourceError
from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype
from apps.bi import model_enums

logger = log_utils.get_logging(name='model', file_name='model.log')


class GaugeChart(BaseChart):
    name = model_enums.CHART_TTYPE_GAUGE

    def hook_label_formatter(self, formatter_kwargs):
        super(GaugeChart, self).hook_label_formatter(formatter_kwargs)
        formatter_kwargs.update(dict(ttype="num", millesimal=False))

    def hook_tooltip_formatter(self, formatter_kwargs):
        super(GaugeChart, self).hook_tooltip_formatter(formatter_kwargs)
        formatter_kwargs.update(dict(ttype="num", millesimal=False))

    @BaseChart.delete_df_already_used_column
    async def to_option(self):
        await self.create(self.dbchart)

        self.get_base_chart_option()

        try:
            await self.get_filtered_df()
        except ResourceError as e:
            return self.option, self.chart_option

        await self.get_index()

        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_N_INDEX,
                          Vtype.Y_VALUE_Y_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX,
                          Vtype.Y_VALUE_Y_COLOR_Y_INDEX, Vtype.N_VALUE_N_COLOR_Y_INDEX]:
            return self.option, self.chart_option
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_N_COLOR_Y_INDEX]:
            await self.get_df()
            series_list = []
            result = self.dh.get_pivot_data_result()
            for i, head_value in enumerate(result["head"]["value"]):
                series_option = self.get_base_series_option()
                series_option.data = []
                for data in result["data"]:
                    if len(data["value"]) > 0:
                        series_option.data.append({'name': await self._convert_field_name(data["name"]), 'value': self._convert_number_value(data["value"][i])})
                    else:
                        series_option.data.append({'name': await self._convert_field_name(data["name"]), 'value': self._convert_number_value(i)})
                    series_option.field_id = data["name"]
                    series_option.id = data["name"]
                series_option.name = await self._convert_column_value(result["head"]["value"][i], field_list=result["head"]["name"])
                series_list.append(series_option)
        else:
            return self.option, self.chart_option

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

        await self.set_option_series_formatter()
        await self.set_option_axis_line()
        await self.set_option_axis_label()

        self.chart_option.update(dict(
            max=def_max_value,
            min=def_min_value,
            formatterDict=self.formatterDict
        ))
        return self.option, self.chart_option

    @BaseChart.delete_df_already_used_column
    async def to_export_data(self):
        return await super(GaugeChart, self).to_export_data()

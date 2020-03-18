# coding=utf8
from apps.errors import AppResourceError
from exceptions import ResourceError
from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype
from apps.bi import model_enums

logger = log_utils.get_logging(name='model', file_name='model.log')


class IndexCardChart(BaseChart):
    name = model_enums.CHART_TTYPE_INDEX_CARD

    @BaseChart.delete_df_already_used_column
    async def to_option(self):
        await self.create(self.dbchart)

        self.get_base_chart_option()

        try:
            await self.get_filtered_df(self.all_field_list)
        except ResourceError as e:
            return self.option, self.chart_option

        await self.get_index()
        await self.get_df()
        series_list = []
        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_N_INDEX,
                          Vtype.Y_VALUE_Y_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX,
                          Vtype.Y_VALUE_Y_COLOR_Y_INDEX, Vtype.N_VALUE_N_COLOR_Y_INDEX]:
            return self.option, self.chart_option
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_N_COLOR_Y_INDEX]:
            result = self.dh.get_pivot_data_result()
            for i, head_value in enumerate(result["head"]["value"]):
                for data in result["data"]:
                    series_option = self.get_base_series_option()
                    series_option.data = []
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

        await self.set_option_series_formatter()

        self.chart_option.update(dict(
            formatterDict=self.formatterDict
        ))
        return self.option, self.chart_option

    @BaseChart.delete_df_already_used_column
    async def to_export_data(self):
        return await super(IndexCardChart, self).to_export_data()

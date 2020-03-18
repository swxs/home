# coding=utf8

import math

from apps.errors import AppResourceError
from exceptions import ResourceError
from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype
from commons.Helpers.Helper_validate import Validate, RegType
from apps.bi import model_enums
from apps.bi import chart_enums
from apps.bi import field_utils

logger = log_utils.get_logging(name='model', file_name='model.log')


class TableChart(BaseChart):
    name = model_enums.CHART_TTYPE_TABLE

    def __init__(self, dbchart, dh, **params):
        super().__init__(dbchart, dh, **params)
        self.chart_option.update(dict(
            show_type="table"
        ))

    async def set_field_formatter(self, field_id):
        if Validate.check(field_id, reg_type=RegType.COLUMN_ID):
            field = await field_utils.get_field(field_id)
            formatter_kwargs = self._get_formatter_dict(field, key="default_field_formatter")
            self.formatterDict[field_id] = self._get_formatter_lastdict(**formatter_kwargs)
        else:
            logger.error("{chart_name}: {field_id} is not a field_id!".format(chart_name=self.dbchart.title or self.dbchart.name, field_id=field_id))

    @BaseChart.delete_df_already_used_column
    async def to_option(self):
        await self.create(self.dbchart)

        try:
            await self.get_filtered_df()
        except ResourceError as e:
            return {"columns": [], "data": []}, self.chart_option
        await self.get_index()

        page = self.custom_attr.get('page', 1)
        page_number = self.dbchart.custom_attr.get('page_number', 20)
        data_start = (page - 1) * page_number
        if self.dbchart.custom_attr and self.dbchart.custom_attr.get('cut_page', False):
            data_end = page * page_number
        else:
            data_end = None

        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_N_INDEX]:
            return dict(columns=[], data=[]), self.chart_option
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_Y_COLOR_N_INDEX]:
            await self.get_df()
            await self.get_ranked_df()
            result = self.dh.get_pivot_data_result()
            columns = list()
            data = list()
            data_dict = dict()
            for result_data in result["data"]:
                column_name = await self._convert_field_name(result_data["name"])
                columns.append({
                    "title": column_name,
                    "key": column_name,
                    "field_id": result_data["name"],
                    "is_index": False,
                })
                data_dict[column_name] = self._convert_string_value(result_data["value"][0])
                await self.set_field_formatter(result_data["name"])
            data.append(data_dict)

            self.chart_option.update(dict(
                formatterDict=self.formatterDict
            ))
            return dict(columns=columns, data=data), self.chart_option
        elif self.vtype in [Vtype.N_VALUE_N_COLOR_Y_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX]:
            """
            只有维度时获取原始数据
            """
            if self.dbchart.custom_attr is not None and self.dbchart.custom_attr.get("showChartSort", False):
                if self.dbchart.custom_attr.get("xAxisLimit", False):
                    x_axis_count = self.dbchart.custom_attr.get("xAxisCount", None)
                    if (not data_end) or (x_axis_count < data_end):
                        data_end = x_axis_count
                else:
                    x_axis_count = None

            result = await self.dh.get_raw_data_result(
                [field.id for field in self.index_list],
                start=data_start,
                end=data_end
            )
            columns = [
                dict(
                    title=await self._convert_field_name(field_id),
                    key=await self._convert_field_name(field_id),
                    field_id=field_id,
                    is_index=True,
                    index_level=i
                )
                for i, field_id in enumerate(result["head"]["value"])
            ]

            data = list()
            for result_data in result["data"]:
                data_dict = dict()
                for i, value in enumerate(result_data["value"]):
                    data_dict[columns[i]['title']] = await self._convert_column_value(value, field_id=columns[i]['field_id'])
                data.append(data_dict)

            self.chart_option.update(dict(
                page=page,
                page_number=page_number,
                all_page=math.ceil(result["info"]["length"] / float(page_number)),
                formatterDict=self.formatterDict
            ))
            return dict(columns=columns, data=data), self.chart_option
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_Y_INDEX, Vtype.Y_VALUE_Y_COLOR_Y_INDEX]:
            await self.get_df()
            await self.get_ranked_df()
            result = self.dh.get_pivot_data_as_raw_data_result(start=data_start, end=data_end)

            columns = list()
            for i, field_id in enumerate(result["head"]["value"]):
                is_index = await self._is_index(field_id)
                if is_index and hasattr(self, "drilldown_level"):
                    drilldown_level = self.drilldown_level
                else:
                    drilldown_level = i
                column_name = await self._convert_field_name(field_id)
                columns.append(dict(
                    title=column_name,
                    key=column_name,
                    field_id=field_id,
                    is_index=is_index,
                    index_level=drilldown_level
                ))
                if not is_index:
                    await self.set_field_formatter(field_id)

            data = list()
            for result_data in result["data"]:
                data_dict = dict()
                for i, value in enumerate(result_data["value"]):
                    data_dict[columns[i]['title']] = await self._convert_column_value(value, field_id=columns[i]['field_id'])
                data.append(data_dict)

            self.chart_option.update(dict(
                drill_down_info=await self._get_drilldown_info(),
                page=page,
                page_number=page_number,
                all_page=math.ceil(result["info"]["length"] / float(page_number)),
                formatterDict=self.formatterDict
            ))
            return dict(columns=columns, data=data), self.chart_option
        return {"columns": [], "data": []}, self.chart_option

    @BaseChart.delete_df_already_used_column
    async def to_export_data(self):
        await self.create(self.dbchart)
        await self.get_filtered_df(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
        await self.get_index(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_N_INDEX,
                          Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_Y_COLOR_N_INDEX,
                          Vtype.Y_VALUE_N_COLOR_Y_INDEX, Vtype.Y_VALUE_Y_COLOR_Y_INDEX]:
            return await super(TableChart, self).to_export_data()
        elif self.vtype in [Vtype.N_VALUE_N_COLOR_Y_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX]:
            result = await self.dh.get_raw_data_result(
                [field.id for field in self.index_list]
            )
            headers = await self._get_rawdata_export_headers(result)
            datas = await self._get_rawdata_export_datas(result)
            info_list = [dict(headers=headers, datas=datas, name=self.dbchart.title or self.dbchart.name)]
            return await self.save_data_to_excel(info_list)

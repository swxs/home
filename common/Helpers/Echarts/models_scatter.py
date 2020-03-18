# coding=utf8

import re
import numpy as np
import settings
from apps.errors import AppResourceError
from exceptions import ResourceError
from commons import consts
from commons.Helpers.Helper_optimize import Optimize
from commons.Metaclass.Prototype import Prototype
from commons import log_utils
from commons.Echarts.models_base import BaseChart, Vtype
from commons.Echarts.option_consts import *
from commons.Echarts.option_serie import (
    BaseSeriesOptionOptimize,
    MarkPoint,
    MarkPointLabel,
    MarkPointLabelNormal,
    MarkPointCoord,
    MarkAreaStart,
    MarkAreaEnd,
    MarkAreaStartItemStyle,
    MarkAreaStartLabel,
    MarkAreaStartItemStyleNormal,
    MarkAreaStartLabelNormal,
    ItemStyle,
    ItemStyleNormal
)
from apps.bi import model_enums
from apps.bi import field_utils
from apps.bi import chart_utils
from apps.bi import chart_enums
from collections import defaultdict, namedtuple

logger = log_utils.get_logging(name='model', file_name='model.log')

FIELD_ID_COMPILER = re.compile(r"\(\s*(?P<field_x_id>(None|null|\w{24}))\s*,\s*(?P<field_y_id>(None|null|\w{24}))\s*\)")


class Center(Prototype):
    x = 0
    y = 0


class Desc(Prototype):
    top_left = ""
    top_right = ""
    bottom_left = ""
    bottom_right = ""


class Color(Prototype):
    top_left = "#FFF7ED"
    top_right = "#EEF9F1"
    bottom_left = "#FFEEEE"
    bottom_right = "#FFFDF1"


class Position(Prototype):
    top_left = "top"
    top_right = "top"
    bottom_left = "bottom"
    bottom_right = "bottom"


class ScatterChart(BaseChart):
    name = model_enums.CHART_TTYPE_SCATTER

    def hook_data_zoom(self):
        for dataZoom in self.option.dataZoom:
            dataZoom.start = 0
            dataZoom.end = 100
        super(ScatterChart, self).hook_data_zoom()

    async def set_option_value_visualmap_color(self):
        def _get_text_value(value, base=0):
            return int(value) + base

        for i, series in enumerate(self.option.series):
            field_id = self._get_series_field(series)
            if field_id is None:
                continue
            if not self._has_visual_map(field_id):
                continue
            field = await field_utils.get_field(field_id)
            advanced_color_type = field.custom_attr.get('advanced_color_type', None)
            if (not advanced_color_type) or advanced_color_type == chart_enums.CHART_VMTYPE_NORMAL:
                if field.custom_attr.get('color', None):
                    series.itemStyle.normal.color = field.custom_attr.get('color', None)

    def _get_formatter_funcstr(self, **kwargs):
        if isinstance(kwargs.get("millesimal", False), list):
            return "$$\
this.getNormalFormatterHandler({{\
ttype: ['{ttype_1}', '{ttype_2}'], \
digit: {digit}, \
unit: ['{unit_1}', '{unit_2}'], \
millesimal: [{millesimal_1}, {millesimal_2}], \
showText: {showText}, \
showValue: {showValue}, \
showPercent: {showPercent}, \
usage: '{usage}'\
}})\
$$".format(
                ttype_1=kwargs.get("ttype", ["num", "num"])[0],
                ttype_2=kwargs.get("ttype", ["num", "num"])[1],
                digit=kwargs.get("digit", [2, 2]),  # 这里是个列表， 因为数字不用做转换所以实现形式和上下的不一样
                unit_1=kwargs.get("unit", ["", ""])[0],
                unit_2=kwargs.get("unit", ["", ""])[1],
                millesimal_1=consts.TEXT_BOOLEAN[kwargs.get("millesimal", [False, False])[0]],
                millesimal_2=consts.TEXT_BOOLEAN[kwargs.get("millesimal", [False, False])[1]],
                showText=consts.TEXT_BOOLEAN[kwargs.get("showText", False)],
                showValue=consts.TEXT_BOOLEAN[kwargs.get("showValue", True)],
                showPercent=consts.TEXT_BOOLEAN[kwargs.get("showPercent", True)],
                usage=kwargs.get("usage", None),
            )
        else:
            return "$$\
this.getNormalFormatterHandler({{\
ttype: '{ttype}', \
digit: {digit}, \
unit: '{unit}', \
millesimal: {millesimal}, \
showText: {showText}, \
showValue: {showValue}, \
showPercent: {showPercent}, \
usage: '{usage}'\
}})\
$$".format(
                ttype=kwargs.get("ttype", "num"),
                digit=kwargs.get("digit", 2),
                unit=kwargs.get("unit", ""),
                millesimal=consts.TEXT_BOOLEAN[kwargs.get("millesimal", False)],
                showText=consts.TEXT_BOOLEAN[kwargs.get("showText", False)],
                showValue=consts.TEXT_BOOLEAN[kwargs.get("showValue", True)],
                showPercent=consts.TEXT_BOOLEAN[kwargs.get("showPercent", True)],
                usage=kwargs.get("usage", None),
            )

    def _get_series_field_list(self, series, key_name="field_id"):
        groups = FIELD_ID_COMPILER.match(series.get(key_name, "(None, None)"))
        if groups:
            field_list = list()
            if groups.groupdict()["field_x_id"] not in ["None", "null"]:
                field_list.append(groups.groupdict()["field_x_id"])
            else:
                field_list.append(None)

            if groups.groupdict()["field_y_id"] not in ["None", "null"]:
                field_list.append(groups.groupdict()["field_y_id"])
            else:
                field_list.append(None)

            if field_list == [None, None]:
                return None
            else:
                return field_list
        else:
            return None

    async def set_option_series_formatter(self):
        for series in self.option.series:
            if self._has_color_tag():
                field_list = list()
                if len(self.value_x_list) == 1:
                    field_list.append(self.value_x_list[0])
                else:
                    field_list.append(None)

                if len(self.value_y_list) == 1:
                    field_list.append(self.value_y_list[0])
                else:
                    field_list.append(None)

                if field_list == [None, None]:
                    return None
            else:
                field_id_list = self._get_series_field_list(series)
                if field_id_list is None:
                    return None
                field_list = list()
                for field_id in field_id_list:
                    if field_id is None:
                        field_list.append(None)
                    else:
                        field_list.append(await field_utils.get_field(field_id))

            formatter_kwargs = self._get_formatter_dict(self.dbchart, key="default_x_field_formatter")
            formatter_kwargs["ttype"] = list()
            formatter_kwargs["digit"] = list()
            formatter_kwargs["unit"] = list()
            formatter_kwargs["millesimal"] = list()
            for index, field in enumerate(field_list):
                if field is None:
                    formatter_kwargs["ttype"].append("num")
                    formatter_kwargs["digit"].append(0)
                    formatter_kwargs["unit"].append('')
                    formatter_kwargs["millesimal"].append(False)
                else:
                    if index == 0:
                        default_formatter_kwargs = self._get_formatter_dict(self.dbchart, key="default_x_field_formatter")
                    else:
                        default_formatter_kwargs = self._get_formatter_dict(self.dbchart, key="default_y_field_formatter")
                    field_formatter_kwargs = self._get_formatter_dict(field, key="default_field_formatter")
                    formatter_kwargs["ttype"].append(field_formatter_kwargs.get("ttype", default_formatter_kwargs.get("ttype", "num")))
                    formatter_kwargs["digit"].append(field_formatter_kwargs.get("digit", default_formatter_kwargs.get("digit", 2)))
                    formatter_kwargs["unit"].append(field_formatter_kwargs.get("unit", default_formatter_kwargs.get("unit", '')))
                    formatter_kwargs["millesimal"].append(field_formatter_kwargs.get("millesimal", default_formatter_kwargs.get("millesimal", False)))

            self.hook_label_formatter(formatter_kwargs)
            series.label.normal.formatter = self._get_formatter_funcstr(**formatter_kwargs)

            self.hook_tooltip_formatter(formatter_kwargs)
            series.tooltip.formatter = self._get_formatter_funcstr(**formatter_kwargs)

            self.hook_formatter_dict_formatter(formatter_kwargs)
            self.formatterDict[series.name] = self._get_formatter_lastdict(**formatter_kwargs)

    def hook_legend_icon(self, icon="circle"):
        icon = self.dbchart.custom_attr.get('data_symbol', icon)
        if icon == "invertedTriangle":  # 倒三角
            icon = INVERTEDTRIANGLE_SVG
        elif icon == "fork":  # 叉形
            icon = FORK_SVG
        elif icon == "plus":  # 加号
            icon = PLUS_SVG
        return icon

    def _get_color_tag_mark_line_data(self, line_type, field_id):
        result = self.dh.get_pivot_group_data_result(color_tag=True)

        index = None
        for field in self.value_x_list:
            if field.id == field_id:
                index = 0
        for field in self.value_y_list:
            if field.id == field_id:
                index = 1
        if index is None:
            return None

        all_result_data_list = list(
            value
            if value != settings.NONE_DATA else 0
            for data in result['data'][index]
            for value in data['value']
        )
        if line_type == 'min':
            return min(all_result_data_list)
        elif line_type == 'max':
            return max(all_result_data_list)
        elif line_type == 'average':
            return sum(all_result_data_list) / len(all_result_data_list)

    async def _get_series_index(self, field_id, type_line_data):
        if field_id is None:
            type_line_data.update(valueIndex=0, xAxis=type_line_data["axis"])
            return -1, type_line_data
        # for index, series in enumerate(self.option.series):
        for index, field in enumerate(self.value_x_list):
            if field.id == field_id:
                type_line_data.update(valueIndex=0, xAxis=type_line_data["axis"])
                return index, type_line_data
        for index, field in enumerate(self.value_y_list):
            if field.id == field_id:
                type_line_data.update(yAxis=type_line_data["axis"])
                return index, type_line_data
        type_line_data.update(valueIndex=0, xAxis=type_line_data["axis"])
        return -1, type_line_data

    def _get_series_field(self, series, key_name="field_id"):
        groups = FIELD_ID_COMPILER.match(series.get(key_name, "(None, None)"))
        if groups:
            if groups.groupdict()["field_x_id"] not in ["None", "null"]:
                return groups.groupdict()["field_x_id"]
            elif groups.groupdict()["field_y_id"] not in ["None", "null"]:
                return groups.groupdict()["field_y_id"]
            else:
                return None
        else:
            return None

    async def set_optimize(self):
        if not self.dbchart.custom_attr.get("fitline_show", False):
            return self
        is_show = self.dbchart.custom_attr.get('fitline_func_show', False)

        self.chart_option["optimize"] = list()
        optimize_list = list()
        if self._has_color_tag():
            for series_index, series in enumerate(self.option.series):
                real_series_index = series_index % len(self.option.color)
                if len(self.value_x_list) > 0:
                    field_id = self.value_x_list[0].id
                elif len(self.value_y_list) > 0:
                    field_id = self.value_y_list[0].id
                else:
                    continue
                field = await field_utils.get_field(field_id)
                for optimize in field.custom_attr.get("optimize", []):
                    op = Optimize(optimize["ttype"], *tuple(zip(*(data["value"] for data in series.data))))
                    func, x, y = op.get_optimize()
                    data = list(list(d) for d in zip(x, y))
                    index = len(self.chart_option["optimize"])
                    self.chart_option["optimize"].append({"data": data, "func": func})
                    optimize_list.append(BaseSeriesOptionOptimize(
                        name=series.name,
                        data=f"$$this.scatterRegressionHandler({index}).data$$",
                        markPoint=MarkPoint(
                            label=MarkPointLabel(
                                normal=MarkPointLabelNormal(
                                    show=is_show,
                                    formatter=f"$$this.scatterRegressionHandler({index}).func$$"
                                )
                            ),
                            data=[MarkPointCoord(
                                coord=f"$$this.scatterRegressionHandler({index}).points$$"
                            )]),
                    )())
        else:
            for series_index, series in enumerate(self.option.series):
                real_series_index = series_index % len(self.option.color)
                field_id = self._get_series_field(series)
                if field_id is None:
                    continue
                field = await field_utils.get_field(field_id)
                for optimize in field.custom_attr.get("optimize", []):
                    op = Optimize(optimize["ttype"], *tuple(zip(*(data["value"] for data in series.data))))
                    func, x, y = op.get_optimize()
                    data = list(list(d) for d in zip(x, y))
                    index = len(self.chart_option["optimize"])
                    self.chart_option["optimize"].append({"data": data, "func": func})
                    optimize_list.append(BaseSeriesOptionOptimize(
                        name=series.name,
                        data=f"$$this.scatterRegressionHandler({index}).data$$",
                        markPoint=MarkPoint(
                            label=MarkPointLabel(
                                normal=MarkPointLabelNormal(
                                    show=is_show,
                                    formatter=f"$$this.scatterRegressionHandler({index}).func$$"
                                )
                            ),
                            data=[MarkPointCoord(
                                coord=f"$$this.scatterRegressionHandler({index}).points$$"
                            )]),
                    )())
        self.option.series.extend(optimize_list)
        return self

    async def set_option_mark_area(self):
        center = Center()
        desc = Desc()
        color = Color()
        position = Position()

        is_show = self.dbchart.custom_attr.get("markArea_show", False)
        index = self.dbchart.custom_attr.get("markArea_index", None)
        if index is None:
            return self

        xaxis = self.dbchart.custom_attr.get("markArea_xaxis", "mean")
        if xaxis == "mean":
            if self._has_color_tag():
                center.x = np.mean(list(
                    data["value"][0]
                    if data["value"][0] != settings.NONE_DATA else 0
                    for series in self.option.series
                    for data in series["data"]
                ))
            else:
                center.x = np.mean([data["value"][0] for data in self.option.series[index].data])
        elif xaxis == "custom":
            center.x = self.dbchart.custom_attr.get("markArea_xaxis_value", 0)

        yaxis = self.dbchart.custom_attr.get("markArea_yaxis", "mean")
        if yaxis == "mean":
            if self._has_color_tag():
                center.y = np.mean(list(
                    data["value"][1]
                    if data["value"][1] != settings.NONE_DATA else 0
                    for series in self.option.series
                    for data in series["data"]
                ))
            else:
                center.y = np.mean([data["value"][1] for data in self.option.series[index].data])
        elif yaxis == "custom":
            center.y = self.dbchart.custom_attr.get("markArea_yaxis_value", 0)

        if self.dbchart.custom_attr.get("markArea_desc_show", False):
            if self.dbchart.custom_attr.get("markArea_desc_1"):
                desc.top_right = self.dbchart.custom_attr.get("markArea_desc_1")
            if self.dbchart.custom_attr.get("markArea_desc_2"):
                desc.top_left = self.dbchart.custom_attr.get("markArea_desc_2")
            if self.dbchart.custom_attr.get("markArea_desc_3"):
                desc.bottom_left = self.dbchart.custom_attr.get("markArea_desc_3")
            if self.dbchart.custom_attr.get("markArea_desc_4"):
                desc.bottom_right = self.dbchart.custom_attr.get("markArea_desc_4")

        if self.dbchart.custom_attr.get("markArea_color_1"):
            color.top_right = self.dbchart.custom_attr.get("markArea_color_1")
        if self.dbchart.custom_attr.get("markArea_color_2"):
            color.top_left = self.dbchart.custom_attr.get("markArea_color_2")
        if self.dbchart.custom_attr.get("markArea_color_3"):
            color.bottom_left = self.dbchart.custom_attr.get("markArea_color_3")
        if self.dbchart.custom_attr.get("markArea_color_4"):
            color.bottom_right = self.dbchart.custom_attr.get("markArea_color_4")

        # if self.dbchart.custom_attr.get("markArea_desc_position", True):
        if True:
            position.top_left = 'insideTopLeft'
            position.top_right = 'insideTopRight'
            position.bottom_left = 'insideBottomLeft'
            position.bottom_right = 'insideBottomRight'

        self.option.series[0]['markArea'] = {
            "show": is_show,
            "silent": True,
            "data": [
                [
                    MarkAreaStart(
                        name=desc.top_right,
                        xAxis="$$Number.MAX_VALUE$$",
                        yAxis="$$Number.MAX_VALUE$$",
                        itemStyle=MarkAreaStartItemStyle(
                            color=color.top_right,
                            # normal=MarkAreaStartItemStyleNormal(
                            #     color=color.top_right
                            # )
                        ),
                        label=MarkAreaStartLabel(
                            color="#000",
                            position=position.top_right,
                            # normal=MarkAreaStartLabelNormal(
                            #     color="#000",
                            #     position=position.top_right
                            # )
                        )
                    ),
                    MarkAreaEnd(xAxis=center.x, yAxis=center.y)
                ],
                [
                    MarkAreaStart(
                        name=desc.top_left,
                        xAxis="$$-Number.MAX_VALUE$$",
                        yAxis="$$Number.MAX_VALUE$$",
                        itemStyle=MarkAreaStartItemStyle(
                            color=color.top_left,
                            # normal=MarkAreaStartItemStyleNormal(
                            #     color=color.top_left
                            # )
                        ),
                        label=MarkAreaStartLabel(
                            color="#000",
                            position=position.top_left,
                            # normal=MarkAreaStartLabelNormal(
                            #     color="#000",
                            #     position=position.top_left
                            # )
                        )
                    ),
                    MarkAreaEnd(xAxis=center.x, yAxis=center.y)
                ],
                [
                    MarkAreaStart(
                        name=desc.bottom_left,
                        xAxis="$$-Number.MAX_VALUE$$",
                        yAxis="$$-Number.MAX_VALUE$$",
                        itemStyle=MarkAreaStartItemStyle(
                            color=color.bottom_left,
                            # normal=MarkAreaStartItemStyleNormal(
                            #     color=color.bottom_left
                            # )
                        ),
                        label=MarkAreaStartLabel(
                            color="#000",
                            position=position.bottom_left,
                            # normal=MarkAreaStartLabelNorma`l(
                            #     color="#000",
                            #     position=position.bottom_left
                            # )`
                        )
                    ),
                    MarkAreaEnd(xAxis=center.x, yAxis=center.y)
                ],
                [
                    MarkAreaStart(
                        name=desc.bottom_right,
                        xAxis="$$Number.MAX_VALUE$$",
                        yAxis="$$-Number.MAX_VALUE$$",
                        itemStyle=MarkAreaStartItemStyle(
                            color=color.bottom_right,
                            # normal=MarkAreaStartItemStyleNormal(
                            #     color=color.bottom_right
                            # )
                        ),
                        label=MarkAreaStartLabel(
                            color="#000",
                            position=position.bottom_right,
                            # normal=MarkAreaStartLabelNormal(
                            #     color="#000",
                            #     position=position.bottom_right
                            # )
                        )
                    ),
                    MarkAreaEnd(xAxis=center.x, yAxis=center.y)
                ]
            ]
        }

    async def get_series_list(self):
        series_list = []
        result = self.dh.get_pivot_group_data_result(color_tag=self._has_color())
        self.axis_data_list = [
            await self._convert_column_value(x, field_list=result["head"]["name"])
            for x in result["head"]["value"]
        ]
        self.legend_data_list = []
        if self.colortag is None:
            result_data = {d["name"]: d["value"] for d in result["data"]}
            for index, field_group in enumerate(self.value_field_group):
                series_option = self.get_base_series_option()
                value_name_x = await self._convert_field_name(field_group[0]) if field_group[0] else None
                value_name_y = await self._convert_field_name(field_group[1]) if field_group[1] else None
                if value_name_x is None:
                    legend = f"{value_name_y}"
                elif value_name_y is None:
                    legend = f"{value_name_x}"
                else:
                    legend = f"({value_name_x}, {value_name_y})"
                self.legend_data_list.append(legend)

                if self.dbchart.color_type == model_enums.CHART_COLOR_TYPE_COLOR_VALUE:
                    for color_value in self.color_value_list[index: index + 1]:
                        self._color_series_list.append({
                            "field_id": color_value.id,
                            "name": color_value.name,
                            "data": [self._convert_number_value(value) for value in result_data[color_value.id]]
                        })

                if series_option:
                    if not field_group[0]:
                        series_option.data = [
                            {"name": self.axis_data_list[index], "value": [0, self._convert_number_value(value_y)]}
                            for index, value_y in enumerate(result_data[field_group[1]])
                        ]
                    elif not field_group[1]:
                        series_option.data = [
                            {"name": self.axis_data_list[index], "value": [self._convert_number_value(value_x), 0]}
                            for index, value_x in enumerate(result_data[field_group[0]])
                        ]
                    else:
                        series_option.data = [
                            {"name": self.axis_data_list[index], "value": [self._convert_number_value(value_x), self._convert_number_value(value_y)]}
                            for index, (value_x, value_y) in enumerate(zip(result_data[field_group[0]], result_data[field_group[1]]))
                        ]
                    series_option.field_id = f"({field_group[0]}, {field_group[1]})"
                    series_option.id = f"({field_group[0]}, {field_group[1]})"
                    series_option.name = legend
                    series_list.append(series_option)
        else:
            result_data = defaultdict(list)
            for data in result["data"]:
                for d in data:
                    value_field_id, colortag_value = d["name"].split("\001")
                    result_data[colortag_value].append((value_field_id, d["value"]))

            for name, value_list in result_data.items():
                field_group = self.value_field_group[0]
                series_option = self.get_base_series_option()
                index_name = await self._convert_field_name(name)
                self.legend_data_list.append(index_name)

                if series_option:
                    if not field_group[0]:
                        series_option.data = [
                            {"name": self.axis_data_list[index], "value": [0, self._convert_number_value(value_y)]}
                            for index, value_y in enumerate(value_list[0][1])
                        ]
                    elif not field_group[1]:
                        series_option.data = [
                            {"name": self.axis_data_list[index], "value": [self._convert_number_value(value_x), 0]}
                            for index, value_x in enumerate(value_list[0][1])
                        ]
                    else:
                        series_option.data = [
                            {"name": self.axis_data_list[index], "value": [self._convert_number_value(value_x), self._convert_number_value(value_y)]}
                            for index, (value_x, value_y) in enumerate(zip(value_list[0][1], value_list[1][1]))
                        ]
                    series_option.field_id = index_name
                    series_option.id = index_name
                    series_option.name = index_name
                    series_list.append(series_option)
        self.option.series = series_list

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
        await self.set_option_legend(icon="circle")
        await self.set_option_symbol()
        await self.set_option_x_axis(format=True)
        await self.set_option_y_axis(format=True)
        await self.set_option_data_zoom()
        await self.set_option_series_formatter()
        await self.set_option_mark_line()
        await self.set_option_mark_area()

        await self.set_optimize()
        return self.option, self.chart_option

    @BaseChart.delete_df_already_used_column
    async def to_export_data(self):
        await self.create(self.dbchart)
        info_list = list()
        try:
            if self.dbchart.next_chart_id is not None:
                self.dbchart = await chart_utils.get_chart(self.dbchart.next_chart_id)
                await self.create(self.dbchart)
            await self.get_filtered_df(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
        except ResourceError as e:
            return [dict(headers=[], datas=[[], ], name=self.dbchart.title or self.dbchart.name)]

        if self.dbchart.is_drilldown:
            for level in range(len(self.index_list)):
                await self.get_index(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD, level=level)
                await self.get_df(fillna=0, ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
                result = self.dh.get_pivot_data_as_raw_data_result()
                headers = await self._get_rawdata_export_headers(result)
                data = await self._get_rawdata_export_datas(result)
                info_list.append(dict(headers=headers, datas=data, name=self.dbchart.title or self.dbchart.name))
        else:
            await self.get_index(ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
            await self.get_df(fillna=0, ttype=chart_enums.CHART_DISPLAY_DOWNLOAD)
            result = self.dh.get_pivot_group_data_as_raw_data_result()
            headers = await self._get_rawdata_export_headers(result)
            data = await self._get_rawdata_export_datas(result)
            info_list.append(dict(headers=headers, datas=data, name=self.dbchart.title or self.dbchart.name))
        return await self.save_data_to_excel(info_list)


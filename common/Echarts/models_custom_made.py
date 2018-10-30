# coding=utf8
import math

from api.utils.bi.field import Field
from api.consts.bi import chart as chart_consts
from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class CustomMadeChart(BaseChart):
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        try:
            self.get_filtered_df()
        except NoDataException:
            return {"columns": [], "data": []}, {}
        self.get_index()

        page = self.custom_attr.get('page', 1)
        page_number = self.custom_attr.get('page_number', 20)
        data_start = (page - 1) * page_number
        if self.dbchart.custom_attr and self.dbchart.custom_attr.get('cut_page', False):
            data_end = page * page_number
        else:
            data_end = None

        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_N_INDEX]:
            return {"columns": [], "data": []}, {}
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_Y_COLOR_N_INDEX]:
            self.get_df()
            self.get_ranked_df()
            result = self.dh.get_pivot_data_result()
            columns = list()
            data = list()
            data_dict = dict()
            for result_data in result["data"]:
                columns.append({
                    "title": self._convert_field_name(result_data["name"]),
                    "key": self._convert_field_name(result_data["name"]),
                    "is_index": False,
                })
                data_dict[self._convert_field_name(result_data["name"])] = self._convert_name(result_data["value"][0])
            data.append(data_dict)
            return {"columns": columns, "data": data}, {}
        elif self.vtype in [Vtype.N_VALUE_N_COLOR_Y_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX]:
            result = self.dh.get_raw_data_result(
                [Field.get_field_by_field_id(field.id).oid for field in self.index_list],
                start=data_start,
                end=data_end)
            columns = [dict(title=self._convert_field_name(field_id),
                            key=self._convert_field_name(field_id),
                            field_id=field_id,
                            is_index=True,
                            index_level=i) for i, field_id in enumerate(result["head"]["value"])]
            data = list()
            for result_data in result["data"]:
                data_dict = dict()
                for i, value in enumerate(result_data["value"]):
                    data_dict[columns[i]['title']] = self._convert_column_name(value, field_id=columns[i]['field_id'])
                data.append(data_dict)
            return dict(columns=columns, data=data), dict(page=page,
                                                          page_number=page_number,
                                                          all_page=math.ceil(result["info"]["length"] / float(page_number)))
        elif self.vtype in [Vtype.Y_VALUE_N_COLOR_Y_INDEX, Vtype.Y_VALUE_Y_COLOR_Y_INDEX]:
            self.get_df()
            self.get_ranked_df()
            result = self.dh.get_pivot_data_as_raw_data_result(start=data_start, end=data_end)

            columns = list()
            for i, field_id in enumerate(result["head"]["value"]):
                is_index = self._is_index(field_id)
                drilldown_level = i
                if is_index:
                    if hasattr(self, "drilldown_level"):
                        drilldown_level = self.drilldown_level

                columns.append(dict(title=self._convert_field_name(field_id),
                                key=self._convert_field_name(field_id),
                                field_id=field_id,
                                is_index=is_index,
                                index_level=drilldown_level))

            data = list()
            for result_data in result["data"]:
                data_dict = dict()
                for i, value in enumerate(result_data["value"]):
                    data_dict[columns[i]['title']] = self._convert_column_name(value, field_id=columns[i]['field_id'])
                data.append(data_dict)
            return dict(columns=columns, data=data), dict(page=page,
                                                          page_number=page_number,
                                                          all_page=math.ceil(result["info"]["length"] / float(page_number)))
        return {"columns": [], "data": []}, {}

    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        self.get_filtered_df(ttype=chart_consts.CHART_DOWNLOAD)
        self.get_index(ttype=chart_consts.CHART_DOWNLOAD)
        if self.vtype in [Vtype.N_VALUE_N_COLOR_N_INDEX, Vtype.N_VALUE_Y_COLOR_N_INDEX,
                          Vtype.Y_VALUE_N_COLOR_N_INDEX, Vtype.Y_VALUE_Y_COLOR_N_INDEX,
                          Vtype.Y_VALUE_N_COLOR_Y_INDEX, Vtype.Y_VALUE_Y_COLOR_Y_INDEX]:
            return super(CustomMadeChart, self).to_export_data()
        elif self.vtype in [Vtype.N_VALUE_N_COLOR_Y_INDEX, Vtype.N_VALUE_Y_COLOR_Y_INDEX]:
            result = self.dh.get_raw_data_result(
                [Field.get_field_by_field_id(field.id).oid for field in self.index_list])
            headers = self._get_rawdata_export_headers(result)
            datas = self._get_rawdata_export_datas(result)
            return [dict(headers=headers, datas=datas, name=self.dbchart.name)]

# coding=utf8

import pandas as pd
from api.consts.bi import chart as chart_consts
from api.utils.bi.field import Field
from api.utils.organization.region import Region
from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')


class SortedTableChart(BaseChart):
    def set_field_formatter(self, field_id):
        field = Field.get_field_by_field_id(field_id)
        formatter_kwargs = self._get_formatter_dict(field)
        self.formatterDict[field_id] = self._get_formatter_lastdict(**formatter_kwargs)
    
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        self.success_row_index_list = list()
        
        try:
            self.get_filtered_df()
        except NoDataException:
            return {"columns": [], "data": []}, {}
        self.get_index()
        
        if self.vtype in [Vtype.Y_VALUE_N_COLOR_Y_INDEX, ]:
            self.chart_option = dict()
            self.get_df()
            self.get_ranked_df()
            result = self.dh.get_pivot_data_as_raw_data_result()
            
            columns = list()
            columns.append(dict(title="排名", key="排名", is_index=False, is_sort=True))
            for i, field_id in enumerate(result["head"]["value"]):
                is_index = self._is_index(field_id)
                if is_index and hasattr(self, "drilldown_level"):
                    drilldown_level = self.drilldown_level
                else:
                    drilldown_level = i
                
                if not is_index:
                    self.set_field_formatter(field_id)
                
                columns.append(dict(title=self._convert_field_name(field_id),
                                    key=self._convert_field_name(field_id),
                                    field_id=field_id,
                                    is_index=is_index,
                                    index_level=drilldown_level))
            
            data = list()
            region_name_list = [Region.get_region_by_region_id(region_id).name for region_id in self.region_id_list]
            
            for index, result_data in enumerate(result["data"], 1):
                data_dict = dict()
                data_dict.update({"排名": index})
                for i, value in enumerate(result_data["value"], 1):
                    column_name = self._convert_column_name(value, field_id=columns[i]['field_id'])
                    data_dict[columns[i]['title']] = column_name
                    if column_name in region_name_list:
                        # 前端数据顺序从零开始计算 故index-1
                        self.success_row_index_list.append(index - 1)
                data.append(data_dict)
            
            self.chart_option.update(dict(
                success_row_index_list=self.success_row_index_list,
                formatterDict=self.formatterDict
            ))
            return {"columns": columns, "data": data}, self.chart_option
        return {"columns": [], "data": []}, {}
    
    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        self.get_filtered_df(ttype=chart_consts.CHART_DOWNLOAD)
        self._filtered_df = self.dh.get_filtered_df()
        self.get_index(ttype=chart_consts.CHART_DOWNLOAD)
        data_length = pd.Series.nunique(self._filtered_df[self.value_list[0].id])
        self.get_df(ttype=chart_consts.CHART_DOWNLOAD)
        self.dh.do_rank(1, False, 0, None)
        result = self.dh.get_pivot_data_as_raw_data_result()
        headers = list()
        headers.append("排名")
        for i, field_id in enumerate(result["head"]["value"]):
            headers.append(self._convert_field_name(field_id))
        
        datas = list()
        for index, result_data in enumerate(result["data"]):
            tmp_data = list()
            tmp_data.append(index + 1)
            for i, value in enumerate(result_data["value"]):
                tmp_data.append(self._convert_column_name(value, field_id=result["head"]["value"][i]))
            datas.append(tmp_data)
        return [dict(headers=headers, datas=datas, name=self.dbchart.name)]

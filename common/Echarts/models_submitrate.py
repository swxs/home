# coding=utf8

import pandas as pd
from api.consts.bi import field as field_consts
from api.consts.bi import chart as chart_consts
from api.utils.bi.field import Field
from common.Exceptions import NoDataException
from common.Utils.log_utils import getLogger
from common.Echarts.models_base import BaseChart, Vtype

log = getLogger('models')



class SubmitrateChart(BaseChart):
    def set_option_series_formatter(self):
        formatter_kwargs = dict(ttype="num", digit=2, millesimal=False, showText=False, showAxis=False)
        self.option.series[0]["tooltip"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)
        self.option.series[0]["label"]["normal"]["formatter"] = self._get_formatter_funcstr(**formatter_kwargs)
        self.formatterDict[self.option.series[0].name] = self._get_formatter_lastdict(**formatter_kwargs)
        
    def _get_data(self, ttype=chart_consts.CHART_SHOW):
        self.dbchart.get_changed_df(realtime_filter=self.realtime_filter, region_id_list=self.region_id_list, ttype=ttype)
        start_time = None
        end_time = None
        for filter in self.dh._filter_list:
            if filter.get('ttype') == field_consts.DTYPE_DATETIME:
                start_time = filter.get('value_list', [None, None])[0]
                end_time = filter.get('value_list', [None, None])[1]
        kwarg = dict(survey_id=self.dbchart.worktable.datasource.get_survey_id())
        if start_time:
            kwarg.update(dict(start_time=start_time))
        if end_time:
            kwarg.update(dict(end_time=end_time))
        all_rspd = rspd_utils.get_rspd_data_list_by_cdt(**kwarg).count()
        kwarg.update(dict(status=rspd_enum.RSPD_STATUS_SUCCESS))
        success_rspd = rspd_utils.get_rspd_data_list_by_cdt(**kwarg).count()
        if all_rspd == 0:
            return None
        return success_rspd * 1.0 / all_rspd * 100
    
    @BaseChart.delete_df_already_used_column
    def to_option(self):
        self.get_base_chart_option()
        self.chart_option = dict()
        
        series_option = self.get_base_series_option()
        
        series_option.data.append({'name': "提交率", 'value': self._get_data(ttype=chart_consts.CHART_SHOW)})
        series_option.name = "提交率"
        self.option.series = [series_option, ]
        self.set_option_series_formatter()
        
        self.chart_option.update(dict(
            formatterDict=self.formatterDict
        ))
        return self.option, self.chart_option
    
    @BaseChart.delete_df_already_used_column
    def to_export_data(self):
        return [dict(headers=["提交率"],
                     datas=[[self._get_data(ttype=chart_consts.CHART_DOWNLOAD), ], ],
                     name=self.dbchart.name)]

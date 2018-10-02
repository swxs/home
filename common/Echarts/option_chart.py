# coding=utf8

import copy
from common.Metaclass import Singleton
from tornado.util import ObjectDict
from api.consts.bi import chart as chart_consts


class Prototype(object):
    def __init__(self, value):
        self.value = value
    
    def clone(self, **attr):
        obj = copy.deepcopy(self.value)
        obj.update(attr)
        return ObjectDict(obj)

color = ["#577CAD", "#FFA51B", "#EF635C", "#7FBAC4", "#48A47D", "#BCB52B", "#B46A88", "#B29688", "#9FACA4", "#6B6B6B", ]


class toolbox(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "show": False,
            "feature": {
                "mark": {"show": True},
                "dataView": {"show": True, "readOnly": False},
                "restore": {"show": True},
                "saveAsImage": {"show": True},
                "myShowOption": {
                    "show": True,
                    "title": "编辑",
                    "icon": "image://http://echarts.baidu.com/images/favicon.png",
                    "onclick": "$$self.showOption$$",
                },
                "myGoBack": {
                    "show": False,
                    "title": "返回",
                    "icon": "image://http://echarts.baidu.com/images/favicon.png",
                    "onclick": "$$self.goBack$$",
                },
                "myDownloadData": {
                    "show": True,
                    "title": "下载数据",
                    "icon": "image://http://echarts.baidu.com/images/favicon.png",
                    "onclick": "$$self.downloadData$$",
                }
            }
        }
        super(toolbox, self).__init__(value)


class tooltip_axisPointer(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "type": "shadow"
        }
        super(tooltip_axisPointer, self).__init__(value)


class tooltip_textStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "fontSize": 12
        }
        super(tooltip_textStyle, self).__init__(value)


class tooltip(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "trigger": "axis",
            "extraCssText": "border-radius: 0px;",
            "axisPointer": tooltip_axisPointer().clone(),
            "textStyle": tooltip_textStyle().clone(),
        }
        super(tooltip, self).__init__(value)


class axis_pointer(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "link": {
                "xAxisIndex": "all",
                "yAxisIndex": "all"
            }
        }
        super(axis_pointer, self).__init__(value)


class title_textStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {}
        super(title_textStyle, self).__init__(value)


class title(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "show": False,
            "text": "",
            "x": "center",
            "y": "",
            "textStyle": title_textStyle().clone(fontWeight=700)
        }
        super(title, self).__init__(value)


class legend_textStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "fontSize": 10,
            "lineHeight": 10,
            "padding": 0
        }
        super(legend_textStyle, self).__init__(value)


class legend_pageTextStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {}
        super(legend_pageTextStyle, self).__init__(value)


class legend(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "data": [],
            "show": True,
            "left": "left",
            "itemWidth": 12,
            "itemHeight": 12,
            "padding": 0,
            "itemGap": 5,
            "textStyle": legend_textStyle().clone(),
            "pageTextStyle": legend_pageTextStyle().clone()
        }
        super(legend, self).__init__(value)


class grid(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {}
        super(grid, self).__init__(value)


class common_grid(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "left": 20,
            "right": 20,
            "bottom": 20,
            "top": 40,
            "containLabel": True
        }
        super(common_grid, self).__init__(value)


double_x_grid = [grid().clone(left=100, right=20, top=40, bottom="40%", height="50%"), grid().clone(left=100, right=20, bottom="10%", height="25%")]

double_y_grid = [grid().clone(left=100, width="50%"), grid().clone(right=20, width="25%")]


class index_nameTextStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "color": "#787878",
            "fontSize": 10
        }
        super(index_nameTextStyle, self).__init__(value)


class index_textStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "color": "#787878",
            "fontSize": 10
        }
        super(index_textStyle, self).__init__(value)


class index_axisLine_lineStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "color": "#A6A6A6"
        }
        super(index_axisLine_lineStyle, self).__init__(value)


class index_axisLine(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "show": True,
            "lineStyle": index_axisLine_lineStyle().clone()
        }
        super(index_axisLine, self).__init__(value)


class index_axisLabel(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "show": True,
            "inside": False,
            "textStyle": index_textStyle().clone(),
            "rotate": 0,
        }
        super(index_axisLabel, self).__init__(value)


class index_axis(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "data": None,
            "show": True,
            "name": "",
            "nameLocation": "middle",
            "nameGap": 35,
            "nameTextStyle": index_nameTextStyle().clone(),
            "type": "category",
            "splitNumber": "10",
            "axisLine": index_axisLine().clone(),
            "axisLabel": index_axisLabel().clone(),
            "minInterval": 1,
            "axisTick": {"show": False},
            "boundaryGap": ['10%', '10%'],
            "triggerEvent": True,
            "z": 10
        }
        super(index_axis, self).__init__(value)


class value_nameTextStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "color": "#787878",
            "fontSize": 10
        }
        super(value_nameTextStyle, self).__init__(value)


class value_axisLine(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "show": False,
        }
        super(value_axisLine, self).__init__(value)


class value_axisLabel_textStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "color": "#787878",
            "fontSize": 10
        }
        super(value_axisLabel_textStyle, self).__init__(value)


class value_axisLabel(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "show": True,
            "textStyle": value_axisLabel_textStyle().clone()
        }
        super(value_axisLabel, self).__init__(value)


class value_axisTick(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "show": False,
        }
        super(value_axisTick, self).__init__(value)


class value_splitLine_lineStyle(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "color": "#e9e9e9"
        }
        super(value_splitLine_lineStyle, self).__init__(value)


class value_splitLine(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "lineStyle": value_splitLine_lineStyle().clone(),
        }
        super(value_splitLine, self).__init__(value)


class value_axis(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "show": True,
            "type": "value",
            "scale": False,
            "splitNumber": 5,
            "name": "",
            "nameLocation": "middle",
            "nameGap": 35,
            "nameTextStyle": value_nameTextStyle().clone(),
            "axisLine": value_axisLine().clone(),
            "axisLabel": value_axisLabel().clone(),
            "axisTick": value_axisTick().clone(),
            "splitLine": value_splitLine().clone()
        }
        super(value_axis, self).__init__(value)


class map_axis(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "type": "category",
            "data": [],
            "splitNumber": 1,
            "show": False
        }
        super(map_axis, self).__init__(value)


class visual_map(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "seriesIndex": 0,
            "type": "piecewise",
            "minOpen": True,
            "maxOpen": True,
            "show": False,
            "left": 0,
            "bottom": 0,
            "z": 4,
            "itemWidth": 20,
            "itemHeight": 140,
        }
        super(visual_map, self).__init__(value)


class visualmap_piecewise(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "seriesIndex": 0,
            "type": "piecewise",
            "show": False,
            "left": 0,
            "bottom": 0,
            "z": 4,
            "itemWidth": 12,
            "itemHeight": 12,
            "pieces": []
        }
        super(visualmap_piecewise, self).__init__(value)


class visualmap_continuous(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "seriesIndex": 0,
            "type": "continuous",
            "show": False,
            "left": 0,
            "bottom": 0,
            "itemWidth": 12,
            "itemHeight": 12,
            "inRange": {}
        }
        super(visualmap_continuous, self).__init__(value)


class datazoom_x(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "type": "slider",
            "show": False,
            "bottom": "0%",
            "xAxisIndex": [0],
            "start": 0,
            "end": 100
        }
        super(datazoom_x, self).__init__(value)


class datazoom_y(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "type": "slider",
            "show": False,
            "left": "0%",
            "yAxisIndex": [0],
            "start": 0,
            "end": 100
        }
        super(datazoom_y, self).__init__(value)


class base_chart_option_x_bar(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": title().clone(),
            "legend": legend().clone(),
            "color": color,
            "grid": [common_grid().clone()],
            "xAxis": [index_axis().clone()],
            "yAxis": [value_axis().clone()],
            "dataZoom": [datazoom_x().clone()],
            "visualMap": [],
            "series": [],
            "toolbox": toolbox().clone(),
            "tooltip": tooltip().clone(trigger="item"),
        }
        super(base_chart_option_x_bar, self).__init__(value)


class base_chart_option_x_bar_statck(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": title().clone(),
            "legend": legend().clone(),
            "color": color,
            "grid": [common_grid().clone()],
            "xAxis": [index_axis().clone()],
            "yAxis": [value_axis().clone()],
            "dataZoom": [datazoom_x().clone()],
            "visualMap": [],
            "series": [],
            "toolbox": toolbox().clone(),
            "tooltip": tooltip().clone(),
        }
        super(base_chart_option_x_bar_statck, self).__init__(value)


class base_chart_option_y_bar(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": title().clone(),
            "legend": legend().clone(),
            "color": color,
            "grid": [common_grid().clone()],
            "xAxis": [value_axis().clone()],
            "yAxis": [index_axis().clone()],
            "dataZoom": [datazoom_y().clone()],
            "visualMap": [],
            "series": [],
            "toolbox": toolbox().clone(),
            "tooltip": tooltip().clone(trigger="item"),
        }
        super(base_chart_option_y_bar, self).__init__(value)


class base_chart_option_y_bar_stack(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": title().clone(),
            "legend": legend().clone(),
            "color": color,
            "grid": [common_grid().clone()],
            "xAxis": [value_axis().clone()],
            "yAxis": [index_axis().clone()],
            "dataZoom": [datazoom_y().clone()],
            "visualMap": [],
            "series": [],
            "toolbox": toolbox().clone(),
            "tooltip": tooltip().clone(),
        }
        super(base_chart_option_y_bar_stack, self).__init__(value)


class base_chart_option_x_line(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": title().clone(),
            "legend": legend().clone(),
            "color": color,
            "grid": [common_grid().clone()],
            "xAxis": [index_axis().clone()],
            "yAxis": [value_axis().clone()],
            "dataZoom": [datazoom_x().clone()],
            "visualMap": [],
            "series": [],
            "toolbox": toolbox().clone(),
            "tooltip": tooltip().clone(axisPointer=tooltip_axisPointer().clone(type="line")),
        }
        super(base_chart_option_x_line, self).__init__(value)


class base_chart_option_x_barline(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": title().clone(),
            "legend": legend().clone(),
            "color": color,
            "grid": [common_grid().clone()],
            "xAxis": [index_axis().clone()],
            "yAxis": [value_axis().clone(), value_axis().clone()],
            "dataZoom": [datazoom_x().clone()],
            "visualMap": [],
            "series": [],
            "toolbox": toolbox().clone(),
            "tooltip": tooltip().clone(axisPointer=tooltip_axisPointer().clone(type="cross")),
        }
        super(base_chart_option_x_barline, self).__init__(value)


class base_chart_option_pie(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": title().clone(),
            "legend": legend().clone(),
            "color": color,
            "grid": [common_grid().clone()],
            "series": [],
            "toolbox": toolbox().clone(),
            "tooltip": {
                "trigger": "item",
                "formatter": "{a} <br/>{b} : {c} ({d}%)",
            }
        }
        super(base_chart_option_pie, self).__init__(value)


class base_chart_option_map(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": title().clone(),
            "legend": legend().clone(),
            "color": color,
            "visualMap": [],
            "xAxis": [index_axis().clone(show=False)],
            "series": [],
            "toolbox": toolbox().clone(),
            "tooltip": tooltip().clone(trigger="item"),
        }
        super(base_chart_option_map, self).__init__(value)


class base_chart_option_score_card(Prototype):
    __metaclass__ = Singleton
    
    def __init__(self):
        value = {
            "title": "",
            "series": []
        }
        super(base_chart_option_score_card, self).__init__(value)


base_chart_option_dict = {}


def get_base_chart_option(charttype):
    base_option = base_chart_option_dict.get(charttype)
    if base_option is not None:
        return copy.deepcopy(base_option)
    return None


base_chart_option_scatter = {
    "grid": [common_grid().clone()],
    "title": title().clone(),
    "xAxis": [{
        "splitLine": {
            "lineStyle": {
                "type": "dashed"
            }
        }
    }],
    "yAxis": [{
        "splitLine": {
            "lineStyle": {
                "type": "dashed"
            }
        },
        "scale": True
    }],
    "series": [],
    "legend": legend().clone(),
    "toolbox": toolbox().clone(),
}

base_chart_option_treemap = {
    "title": title().clone(),
    "calculable": False,
    "legend": legend().clone(),
    "series": [],
    "toolbox": toolbox().clone(),
    "tooltip": {
        "trigger": "item",
        "formatter": "{b}: {c}"
    },
}

base_chart_option_radar = {
    "grid": [common_grid().clone()],
    "title": title().clone(),
    "legend": legend().clone(),
    "color": color,
    "radar": {
        "shape": "circle",
        "indicator": [],
        "splitNumber": 5,
    },
    "series": [],
    "toolbox": toolbox().clone(),
    "tooltip": {},
}

base_chart_option_gauge = {
    "series": [],
    "tooltip": {
        "formatter": "{a} <br/>{b} : {c}"
    }
}

base_chart_option_dict[chart_consts.CHART_TYPE_BAR] = base_chart_option_x_bar().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_BAR_STACK] = base_chart_option_x_bar_statck().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_BAR_STACK_PERCENT] = base_chart_option_x_bar_statck().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_HBAR] = base_chart_option_y_bar().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_HBAR_STACK] = base_chart_option_y_bar_stack().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_HBAR_STACK_PERCENT] = base_chart_option_y_bar_stack().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_BARLINE] = base_chart_option_x_barline().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_BARLINE_STACK] = base_chart_option_x_barline().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_LINE] = base_chart_option_x_line().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_LINE_SHADOW] = base_chart_option_x_line().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_LINE_STACK] = base_chart_option_x_line().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_PIE] = base_chart_option_pie().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_MAP] = base_chart_option_map().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_RADAR] = base_chart_option_radar
base_chart_option_dict[chart_consts.CHART_TYPE_SCATTER] = base_chart_option_scatter
base_chart_option_dict[chart_consts.CHART_TYPE_TREEMAP] = base_chart_option_treemap
base_chart_option_dict[chart_consts.CHART_TYPE_GAUGE] = base_chart_option_gauge
base_chart_option_dict[chart_consts.CHART_TYPE_INDEX_CARD] = base_chart_option_score_card().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_SCORE_CARD] = base_chart_option_score_card().clone()
base_chart_option_dict[chart_consts.CHART_TYPE_SUBMITRATE] = base_chart_option_score_card().clone()

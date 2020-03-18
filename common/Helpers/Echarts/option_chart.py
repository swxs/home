# -*- coding: utf-8 -*-

import copy
from apps.bi import model_enums
from commons.Metaclass.Prototype import Prototype

color = [
    "#8AC24B",
    "#FFC642",
    "#478AFF",
    "#81C782",
    "#F5805B",
    "#D0B6FF",
    "#3C9CFF",
    "#FFAB31",
    "#B487FF",
    "#7C4DFF",
    "#60B7FF",
    "#FFD868"
]


class toolbox(Prototype):
    show = False
    feature = {
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

class testStyle(Prototype):
    fontFamily = "Arial"


class tooltip_axisPointer(Prototype):
    type = "shadow"


class tooltip_textStyle(Prototype):
    fontSize = 14
    lineHeight = 18
    color = "rgba(96,98,102,1)"


class tooltip(Prototype):
    trigger = "axis"
    padding = [16, 16, 16, 16]
    extraCssText = "border-radius: 0px;"
    backgroundColor = "rgba(255,255,255,1)"
    borderColor = "rgba(239,241,247,1)"
    borderWidth = 1
    axisPointer = tooltip_axisPointer()
    textStyle = tooltip_textStyle()
    extraCssText = 'box-shadow: 0 0 3px rgba(239,241,247,0.2);border-radius: 2px;'


class axis_pointer(Prototype):
    link = {
        "xAxisIndex": "all",
        "yAxisIndex": "all"
    }


class title_textStyle(Prototype):
    fontWeight = 400


class title(Prototype):
    show = False
    text = ""
    x = "center"
    y = ""
    textStyle = title_textStyle(fontWeight=700)


class legend_textStyle(Prototype):
    color = "#909399"
    fontSize = 12
    lineHeight = 12
    padding = [
        1, 0, 0, 1
    ]


class legend_pageTextStyle(Prototype):
    color = "#909399"


class legend(Prototype):
    data = []
    show = True
    type = "scroll"
    # left = "left"
    left = 10
    itemWidth = 10
    itemHeight = 10
    padding = 0
    itemGap = 20
    pageIconSize = 12
    textStyle = legend_textStyle()
    pageTextStyle = legend_pageTextStyle()
    pageIconColor = "#909399"
    pageIconInactiveColor = "#D3D6DE"


class grid(Prototype):
    pass


class common_grid(Prototype):
    left = 0
    right = 0
    bottom = 0
    top = 12
    containLabel = True


class index_nameTextStyle(Prototype):
    color = "#909399"
    fontSize = 10


class index_textStyle(Prototype):
    color = "#909399"
    fontSize = 10


class index_axisLine_lineStyle(Prototype):
    color = "#E1E4EB"


class index_axisLine(Prototype):
    show = True
    lineStyle = index_axisLine_lineStyle()


class index_axisLabel(Prototype):
    show = True
    inside = False
    textStyle = index_textStyle()
    rotate = 0


class index_splitLine(Prototype):
    show = False


class index_axis(Prototype):
    data = None
    show = True
    name = ""
    nameLocation = "middle"
    nameGap = 25
    nameTextStyle = index_nameTextStyle()
    type = "category"
    axisLine = index_axisLine()
    axisLabel = index_axisLabel()
    splitLine = index_splitLine()
    minInterval = 1
    axisTick = {"show": False}
    boundaryGap = ['10%', '10%']
    triggerEvent = True
    z = 10


class value_nameTextStyle(Prototype):
    color = "#909399"
    fontSize = 10


class value_axisLine_lineStyle(Prototype):
    color = "#E1E4EB"


class value_axisLine(Prototype):
    show = False
    lineStyle = value_axisLine_lineStyle()


class value_axisLabel_textStyle(Prototype):
    color = "#909399"
    fontSize = 10


class value_axisLabel(Prototype):
    show = True
    textStyle = value_axisLabel_textStyle()


class value_axisTick(Prototype):
    show = False


class value_splitLine_lineStyle(Prototype):
    color = "#e9e9e9"


class value_splitLine(Prototype):
    show = True
    lineStyle = value_splitLine_lineStyle()


class value_axis(Prototype):
    show = True
    type = "value"
    scale = False
    splitNumber = 5
    name = ""
    nameLocation = "middle"
    nameGap = 25
    nameTextStyle = value_nameTextStyle()
    axisLine = value_axisLine()
    axisLabel = value_axisLabel()
    axisTick = value_axisTick()
    splitLine = value_splitLine()


class map_axis(Prototype):
    type = "category"
    data = []
    show = False


class visual_map(Prototype):
    seriesIndex = 0
    type = "piecewise"
    minOpen = True
    maxOpen = True
    show = False
    left = 0
    bottom = 0
    z = 4
    itemWidth = 20
    itemHeight = 140


class visualmap_piecewise(Prototype):
    seriesIndex = 0
    type = "piecewise"
    show = False
    left = 0
    bottom = 0
    z = 4
    itemWidth = 12
    itemHeight = 12
    pieces = []


class visualmap_continuous(Prototype):
    seriesIndex = 0
    type = "continuous"
    show = False
    left = 0
    bottom = 0
    itemWidth = 12
    itemHeight = 12
    inRange = {}


class datazoom_x(Prototype):
    type = "slider"
    show = False
    bottom = "0%"
    xAxisIndex = [0]
    start = 0
    end = 100


class datazoom_y(Prototype):
    type = "slider"
    show = False
    left = "0%"
    yAxisIndex = [0]
    start = 0
    end = 100


class base_chart_option_x_bar(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    xAxis = [index_axis()]
    yAxis = [value_axis()]
    dataZoom = [datazoom_x()]
    visualMap = []
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip(trigger="item")


class base_chart_option_x_bar_statck(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    xAxis = [index_axis()]
    yAxis = [value_axis()]
    dataZoom = [datazoom_x()]
    visualMap = []
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip()


class base_chart_option_y_bar(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    xAxis = [value_axis()]
    yAxis = [index_axis()]
    dataZoom = [datazoom_y()]
    visualMap = []
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip(trigger="item")


class base_chart_option_y_bar_stack(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    xAxis = [value_axis()]
    yAxis = [index_axis()]
    dataZoom = [datazoom_y()]
    visualMap = []
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip()


class base_chart_option_x_line(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    xAxis = [index_axis()]
    yAxis = [value_axis()]
    dataZoom = [datazoom_x()]
    visualMap = []
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip(axisPointer=tooltip_axisPointer(type="line"))


class base_chart_option_x_barline(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    xAxis = [index_axis()]
    yAxis = [value_axis(), value_axis()]
    dataZoom = [datazoom_x()]
    visualMap = []
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip(axisPointer=tooltip_axisPointer(type="cross"))


class base_chart_option_pie(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip(trigger="item")


class base_chart_option_map(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    visualMap = []
    xAxis = [index_axis(show=False)]
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip(trigger="item")


class base_chart_option_score_card(Prototype):
    title = ""
    series = []
    testStyle = testStyle()


class base_chart_option_scatter(Prototype):
    title = title()
    legend = legend()
    color = color
    grid = [common_grid()]
    xAxis = [value_axis()]
    yAxis = [value_axis()]
    dataZoom = [datazoom_x(), datazoom_y()]
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip(trigger="item")
    visualMap = []


class base_chart_option_treemap(Prototype):
    title = title()
    calculable = False
    legend = legend()
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = tooltip(trigger="item")


class base_chart_option_radar(Prototype):
    grid = [common_grid()]
    title = title()
    legend = legend()
    color = color
    radar = {
        "shape": "circle",
        "indicator": [],
        "splitNumber": 5,
    }
    series = []
    testStyle = testStyle()
    toolbox = toolbox()
    tooltip = {}


class base_chart_option_gauge(Prototype):
    series = []
    tooltip = {
        "formatter": "{a} <br/>{b} : {c}"
    }


base_chart_option_dict = {}

double_x_grid = [
    grid(left=100, right=20, top=40, bottom="40%", height="50%")(),
    grid(left=100, right=20, bottom="10%", height="25%")()
]

double_y_grid = [
    grid(left=100, width="50%")(),
    grid(right=20, width="25%")()
]


def get_base_chart_option(charttype):
    base_option = base_chart_option_dict.get(charttype)
    if base_option is not None:
        if isinstance(base_option, Prototype):
            return base_option()
        else:
            return copy.deepcopy(base_option)
    return None


base_chart_option_dict[model_enums.CHART_TTYPE_BAR] = base_chart_option_x_bar()
base_chart_option_dict[model_enums.CHART_TTYPE_BAR_STACK] = base_chart_option_x_bar_statck()
base_chart_option_dict[model_enums.CHART_TTYPE_BAR_STACK_PERCENT] = base_chart_option_x_bar_statck()
base_chart_option_dict[model_enums.CHART_TTYPE_HBAR] = base_chart_option_y_bar()
base_chart_option_dict[model_enums.CHART_TTYPE_HBAR_STACK] = base_chart_option_y_bar_stack()
base_chart_option_dict[model_enums.CHART_TTYPE_HBAR_STACK_PERCENT] = base_chart_option_y_bar_stack()
base_chart_option_dict[model_enums.CHART_TTYPE_BARLINE] = base_chart_option_x_barline()
base_chart_option_dict[model_enums.CHART_TTYPE_BARLINE_STACK] = base_chart_option_x_barline()
base_chart_option_dict[model_enums.CHART_TTYPE_LINE] = base_chart_option_x_line()
base_chart_option_dict[model_enums.CHART_TTYPE_LINE_SHADOW] = base_chart_option_x_line()
base_chart_option_dict[model_enums.CHART_TTYPE_LINE_STACK] = base_chart_option_x_line()
base_chart_option_dict[model_enums.CHART_TTYPE_PIE] = base_chart_option_pie()
base_chart_option_dict[model_enums.CHART_TTYPE_MAP] = base_chart_option_map()
base_chart_option_dict[model_enums.CHART_TTYPE_RADAR] = base_chart_option_radar()
base_chart_option_dict[model_enums.CHART_TTYPE_SCATTER] = base_chart_option_scatter()
base_chart_option_dict[model_enums.CHART_TTYPE_GAUGE] = base_chart_option_gauge()
base_chart_option_dict[model_enums.CHART_TTYPE_INDEX_CARD] = base_chart_option_score_card()

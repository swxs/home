# -*- coding: utf-8 -*-

import copy
from apps.bi import model_enums as bi_consts
from commons.Metaclass.Prototype import Prototype


class LabelNormal(Prototype):
    show = True
    formatter = None


class LabelEmphasis(Prototype):
    show = True
    formatter = None


class Label(Prototype):
    normal = LabelNormal()
    emphasis = LabelEmphasis()

class AxisLabel(Prototype):
    show = True


class AxisLineLineStyle(Prototype):
    width = 20

class AxisLine(Prototype):
    lineStyle = AxisLineLineStyle()


class SplitLine(Prototype):
    length = 20


class AxisTick(Prototype):
    length = 6


class AreaStyleNormal(Prototype):
    opacity = 0.4


class AreaStyle(Prototype):
    normal = AreaStyleNormal()


class ItemStyleNormal(Prototype):
    color = None
    formatter = None


class ItemStyleEmphasis(Prototype):
    formatter = None


class ItemStyle(Prototype):
    normal = ItemStyleNormal()
    emphasis = ItemStyleEmphasis()


class LabelLineNormal(Prototype):
    show = False


class LabelLineEmphasis(Prototype):
    show = False


class LabelLine(Prototype):
    normal = LabelLineNormal()
    emphasis = LabelLineEmphasis()


class Tooltip(Prototype):
    formatter = None


class MarkLineLabelNormal(Prototype):
    position = "left"
    show = True
    formatter = "{c}"
    fontStyle = 'normal'
    fontSize = 12
    padding = [4, 4]


class MarkLineLabel(Prototype):
    normal = MarkLineLabelNormal()


class MarkLine(Prototype):
    data = []
    label = MarkLineLabel()


class BaseSeriesOptionBar(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    barGap = "10%"
    animation = False
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionBarStack(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    animation = False
    stack = "stack"
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionBarStackPercent(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    animation = False
    stack = "stack"
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionHbar(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    barGap = "10%"
    animation = False
    label = Label(normal=LabelNormal(position="insideLeft", textBorderWidth=2, color=None))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionHbarStack(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    barGap = "10%"
    animation = False
    stack = "stack"
    label = Label(normal=LabelNormal(position="insideLeft", textBorderWidth=2, color=None))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionHbarStackPercent(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    barGap = "10%"
    animation = False
    stack = "stack"
    label = Label(normal=LabelNormal(position="insideLeft", textBorderWidth=2, color=None))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionBarline(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    barGap = "10%"
    animation = False
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionBarlineStack(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    animation = False
    stack = "stack"
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionLine(Prototype):
    name = ""
    type = "line"
    symbol = "emptyCircle"
    showSymbol = False
    showAllSymbol = True
    smooth = False
    animation = False
    itemStyle = ItemStyle(normal=ItemStyleNormal(show=False))
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionLineShadow(Prototype):
    name = ""
    type = "line"
    symbol = "emptyCircle"
    showSymbol = False
    showAllSymbol = True
    smooth = False
    animation = False
    itemStyle = ItemStyle(normal=ItemStyleNormal(show=False))
    areaStyle = AreaStyle()
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionLineStack(Prototype):
    name = ""
    type = "line"
    symbol = "emptyCircle"
    showSymbol = False
    showAllSymbol = True
    smooth = False
    animation = False
    stack = "stack"
    itemStyle = ItemStyle(normal=ItemStyleNormal(show=False))
    areaStyle = AreaStyle()
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionBarlineLine(Prototype):
    name = ""
    type = "line"
    symbol = "emptyCircle"
    showSymbol = False
    showAllSymbol = True
    smooth = False
    animation = False
    yAxisIndex = 1
    itemStyle = ItemStyle(normal=ItemStyleNormal(show=False))
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2, color=None))
    markLine = MarkLine()
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionPie(Prototype):
    name = ""
    type = "pie"
    hoverAnimation = False
    minShowLabelAngle = 1
    radius = "80%"
    center = ["50%", "55%"]
    label = Label()
    itemStyle = ItemStyle(normal=ItemStyleNormal(borderWidth=1, borderColor="#fff"), emphasis=ItemStyleEmphasis(shadowBlur=0, shadowOffsetX=0, shadowColor="rgba(0, 0, 0, 0.5)"))
    labelLine = LabelLine(normal=LabelLineNormal(show=True, length=10, length2=7, smooth=True))
    animation = True
    z = 2
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionRadar(Prototype):
    name = ""
    type = "radar"
    animation = False
    symbol = "none"
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionMap(Prototype):
    name = ""
    type = "map"
    mapType = "china"
    selectedMode = "multiple"
    roam = False
    showLegendSymbol = False
    label = LabelLine(normal=LabelLineNormal(length=10, length2=7))
    itemStyle = ItemStyle(emphasis=ItemStyleEmphasis(areaColor="#1B74CF"))
    tooltip = Tooltip()
    top = 0
    bottom = 0
    fieldId = None
    id = None


class BaseSeriesOptionGauge(Prototype):
    name = ""
    radius = '100%'
    tooltip = Tooltip()
    label = Label()
    axisLabel = AxisLabel()
    axisLine = AxisLine()
    splitLine = SplitLine()
    axisTick = AxisTick()
    fieldId = None
    id = None


class BaseSeriesOptionScoreCard(Prototype):
    name = ""
    tooltip = Tooltip()
    label = Label()
    fieldId = None
    id = None


class BaseSeriesOptionSubmitrate(Prototype):
    name = ""
    tooltip = Tooltip()
    label = Label()
    fieldId = None
    id = None


class BaseSeriesOptionScatter(Prototype):
    name = ""
    type = "scatter"
    tooltip = Tooltip()
    label = Label(normal=LabelNormal(position="top"), emphasis=LabelEmphasis(position="top"))
    itemStyle = ItemStyle(normal=LabelNormal())
    symbol = 'circle'
    animation = False
    markLine = MarkLine()
    fieldId = None
    id = None


class BaseSeriesOptionTreemap(Prototype):
    name = ""
    type = "treemap"
    tooltip = Tooltip()
    label = Label()
    itemStyle = ItemStyle(normal=ItemStyleNormal(borderWidth=1))
    animation = False
    fieldId = None
    id = None


class BaseSeriesOptionGridBar(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    barGap = "10%"
    label = Label(normal=LabelNormal(position="insideBottom", align="center", textBorderWidth=2))
    itemStyle = ItemStyle()
    markLine = MarkLine()
    animation = False
    xAxisIndex = 1
    yAxisIndex = 1
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionGridHbar(Prototype):
    name = ""
    type = "bar"
    barMaxWidth = "100"
    barGap = "10%"
    label = Label(normal=LabelNormal(position="insideLeft", textBorderWidth=2))
    itemStyle = ItemStyle()
    animation = False
    markLine = MarkLine()
    xAxisIndex = 1
    yAxisIndex = 1
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionGridLine(Prototype):
    name = ""
    type = "line"
    barMaxWidth = "100"
    barGap = "10%"
    label = Label(normal=LabelNormal(position="top", textBorderWidth=2))
    itemStyle = ItemStyle()
    animation = False
    markLine = MarkLine()
    xAxisIndex = 1
    yAxisIndex = 1
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionGridCustomText(Prototype):
    name = ""
    type = "custom_text"
    barMaxWidth = "100"
    barGap = "10%"
    label = Label(normal=LabelNormal(position="top", textBorderWidth=2))
    itemStyle = ItemStyle()
    animation = False
    markLine = MarkLine()
    xAxisIndex = 1
    yAxisIndex = 1
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionTag(Prototype):
    name = ""
    type = "custom"
    barMaxWidth = "100"
    barGap = "10%"
    label = Label(normal=LabelNormal(show=False, textBorderWidth=2))
    itemStyle = ItemStyle()
    animation = False
    tooltip = Tooltip()
    fieldId = None
    id = None


class BaseSeriesOptionIndexCard(Prototype):
    fieldId = None
    id = None
    label = Label(normal=LabelNormal())
    tooltip = Tooltip()


class MarkPointItemStyleNormal(Prototype):
    color = "transparent"


class MarkPointItemStyle(Prototype):
    normal = MarkPointItemStyleNormal()


class MarkPointLabelNormal(Prototype):
    show = True
    position = "left"
    formatter = "$$this.scatterRegressionHandler().expression$$"
    textStyle = {
        "color": '#333',
        "fontSize": 14
    }


class MarkPointLabel(Prototype):
    normal = MarkPointLabelNormal()


class MarkPointCoord(Prototype):
    coord = "$$this.scatterRegressionHandler().points$$"


class MarkPoint(Prototype):
    itemStyle = MarkPointItemStyle()
    label = MarkPointLabel()
    data = [MarkPointCoord()]


class BaseSeriesOptionOptimize(Prototype):
    """
    拟合线设置
    """
    name = "line"
    type = "line"
    showSymbol = False
    smooth = True
    data = "$$this.scatterRegressionHandler().data"
    itemstyle = ItemStyle()
    markPoint = MarkPoint()


class MarkAreaStartItemStyleNormal(Prototype):
    color = 'rgba(255, 0, 0, 0.1)'


class MarkAreaStartItemStyle(Prototype):
    color = 'rgba(255, 0, 0, 0.1)'
    # normal = MarkAreaStartItemStyleNormal()


class MarkAreaStartLabelNormal(Prototype):
    # distance = -20
    pass


class MarkAreaStartLabel(Prototype):
    color = "#000"
    position = "insideTopLeft"
    # normal = MarkAreaStartLabelNormal()


class MarkAreaStart(Prototype):
    name = "A区"
    xAxis = 'max'
    yAxis = 'max'
    itemStyle = MarkAreaStartItemStyle()
    label = MarkAreaStartLabel()


class MarkAreaEnd(Prototype):
    xAxis = 'max'
    yAxis = 'max'


BASE_SERIES_OPTION_DICT = dict()


def get_base_series_option(series_type):
    base_option = BASE_SERIES_OPTION_DICT.get(series_type)
    if base_option is not None:
        if isinstance(base_option, Prototype):
            return base_option()
        else:
            return copy.deepcopy(base_option)
    return None


BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_BAR] = BaseSeriesOptionBar()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_BAR_STACK] = BaseSeriesOptionBarStack()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_BAR_STACK_PERCENT] = BaseSeriesOptionBarStackPercent()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_HBAR] = BaseSeriesOptionHbar()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_HBAR_STACK] = BaseSeriesOptionHbarStack()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_HBAR_STACK_PERCENT] = BaseSeriesOptionHbarStackPercent()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_BARLINE] = BaseSeriesOptionBarline()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_BARLINE_STACK] = BaseSeriesOptionBarlineStack()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_BARLINE_LINE] = BaseSeriesOptionBarlineLine()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_LINE] = BaseSeriesOptionLine()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_LINE_SHADOW] = BaseSeriesOptionLineShadow()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_LINE_STACK] = BaseSeriesOptionLineStack()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_PIE] = BaseSeriesOptionPie()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_MAP] = BaseSeriesOptionMap()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_GAUGE] = BaseSeriesOptionGauge()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_RADAR] = BaseSeriesOptionRadar()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_SCATTER] = BaseSeriesOptionScatter()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_INDEX_CARD] = BaseSeriesOptionIndexCard()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_SUB_BAR] = BaseSeriesOptionBar()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_SUB_LINE] = BaseSeriesOptionLine()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_GRID_BAR] = BaseSeriesOptionGridBar()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_GRID_HBAR] = BaseSeriesOptionGridHbar()
BASE_SERIES_OPTION_DICT[bi_consts.FIELD_TTYPE_GRID_LINE] = BaseSeriesOptionGridLine()

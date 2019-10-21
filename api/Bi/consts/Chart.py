# -*- coding: utf-8 -*-
# @File    : Chart.py
# @AUTH    : model_creater

CHART_TTYPE_BAR = 1
CHART_TTYPE_BAR_STACK = 2
CHART_TTYPE_BAR_STACK_PERCENT = 3
CHART_TTYPE_HBAR = 4
CHART_TTYPE_HBAR_STACK = 5
CHART_TTYPE_HBAR_STACK_PERCENT = 6
CHART_TTYPE_BARLINE = 7
CHART_TTYPE_BARLINE_STACK = 8
CHART_TTYPE_LINE = 9
CHART_TTYPE_LINE_SHADOW = 10
CHART_TTYPE_LINE_STACK = 11
CHART_TTYPE_PIE = 12
CHART_TTYPE_RADAR = 13
CHART_TTYPE_SCATTER = 14
CHART_TTYPE_MAP = 15
CHART_TTYPE_GAUGE = 16
CHART_TTYPE_INDEX_CARD = 17
CHART_TTYPE_TABLE = 18
CHART_TTYPE_RICHTEXT = 19
CHART_TTYPE_CUSTOM_MADE = 20

CHART_TTYPE_LIST = [
    (CHART_TTYPE_BAR, '柱状图'),
    (CHART_TTYPE_BAR_STACK, '堆积柱状图'),
    (CHART_TTYPE_BAR_STACK_PERCENT, '百分比堆积柱状图'),
    (CHART_TTYPE_HBAR, '条形图'),
    (CHART_TTYPE_HBAR_STACK, '堆积条形图'),
    (CHART_TTYPE_HBAR_STACK_PERCENT, '百分比堆积条形图'),
    (CHART_TTYPE_BARLINE, '柱状折线图'),
    (CHART_TTYPE_BARLINE_STACK, '堆积柱状折线图'),
    (CHART_TTYPE_LINE, '折线图'),
    (CHART_TTYPE_LINE_SHADOW, '折线阴影图'),
    (CHART_TTYPE_LINE_STACK, '堆积折线图'),
    (CHART_TTYPE_PIE, '饼图'),
    (CHART_TTYPE_RADAR, '雷达图'),
    (CHART_TTYPE_SCATTER, '散点图'),
    (CHART_TTYPE_MAP, '地图'),
    (CHART_TTYPE_GAUGE, '仪表盘'),
    (CHART_TTYPE_INDEX_CARD, '指标卡'),
    (CHART_TTYPE_TABLE, '表格'),
    (CHART_TTYPE_RICHTEXT, '富文本'),
    (CHART_TTYPE_CUSTOM_MADE, '私人定制'),
]
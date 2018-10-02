# coding=utf8

from api.consts.bi import chart as chart_consts
from common.Echarts.models_bar import BarChart
from common.Echarts.models_bar_stack import BarStackChart
from common.Echarts.models_bar_stack_percent import BarStackPercentChart

from common.Echarts.models_hbar import HbarChart
from common.Echarts.models_hbar_stack import HbarStackChart
from common.Echarts.models_hbar_stack_percent import HbarStackPercentChart

from common.Echarts.models_barline import BarlineChart
from common.Echarts.models_barline_stack import BarlineStackChart

from common.Echarts.models_line import LineChart
from common.Echarts.models_line_stack import LineStackChart
from common.Echarts.models_line_shadow import LineShadowChart

from common.Echarts.models_pie import PieChart
from common.Echarts.models_radar import RadarChart
from common.Echarts.models_scatter import ScatterChart
from common.Echarts.models_tree_map import TreeMapChart
from common.Echarts.models_table import TableChart
from common.Echarts.models_gauge import GaugeChart
from common.Echarts.models_map import MapChart
from common.Echarts.models_score_card import ScoreCardChart
from common.Echarts.models_index_card import IndexCardChart

from common.Echarts.models_custom_made import CustomMadeChart
from common.Echarts.models_submitrate import SubmitrateChart
from common.Echarts.models_sorted_table import SortedTableChart

from common.Utils.log_utils import getLogger

log = getLogger('models.py')

ChartModelDict = {}

ChartModelDict[chart_consts.CHART_TYPE_BAR] = BarChart
ChartModelDict[chart_consts.CHART_TYPE_BAR_STACK] = BarStackChart
ChartModelDict[chart_consts.CHART_TYPE_BAR_STACK_PERCENT] = BarStackPercentChart

ChartModelDict[chart_consts.CHART_TYPE_HBAR] = HbarChart
ChartModelDict[chart_consts.CHART_TYPE_HBAR_STACK] = HbarStackChart
ChartModelDict[chart_consts.CHART_TYPE_HBAR_STACK_PERCENT] = HbarStackPercentChart

ChartModelDict[chart_consts.CHART_TYPE_BARLINE] = BarlineChart
ChartModelDict[chart_consts.CHART_TYPE_BARLINE_STACK] = BarlineStackChart

ChartModelDict[chart_consts.CHART_TYPE_LINE] = LineChart
ChartModelDict[chart_consts.CHART_TYPE_LINE_STACK] = LineStackChart
ChartModelDict[chart_consts.CHART_TYPE_LINE_SHADOW] = LineShadowChart

ChartModelDict[chart_consts.CHART_TYPE_PIE] = PieChart

ChartModelDict[chart_consts.CHART_TYPE_TABLE] = TableChart

ChartModelDict[chart_consts.CHART_TYPE_GAUGE] = GaugeChart
ChartModelDict[chart_consts.CHART_TYPE_MAP] = MapChart
ChartModelDict[chart_consts.CHART_TYPE_SCORE_CARD] = ScoreCardChart

ChartModelDict[chart_consts.CHART_TYPE_INDEX_CARD] = IndexCardChart

ChartModelDict[chart_consts.CHART_TYPE_RADAR] = RadarChart

ChartModelDict[chart_consts.CHART_TYPE_SCATTER] = ScatterChart

ChartModelDict[chart_consts.CHART_TYPE_TREEMAP] = TreeMapChart
ChartModelDict[chart_consts.CHART_TYPE_CUSTOM_MADE] = CustomMadeChart
ChartModelDict[chart_consts.CHART_TYPE_SUBMITRATE] = SubmitrateChart
ChartModelDict[chart_consts.CHART_TYPE_SORTED_TABLE] = SortedTableChart

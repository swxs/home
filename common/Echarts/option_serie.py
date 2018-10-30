# coding=utf8

import copy
from api.consts.bi import field as field_consts

base_serie_option_dict = {}


def get_base_serie_option(serietype):
    base_option = base_serie_option_dict.get(serietype)
    if base_option is not None:
        return copy.deepcopy(base_option)
    return None


base_serie_option_bar = {
    "name": "",
    "type": "bar",
    "barMaxWidth": "100",
    "barGap": "10%",
    "animation": False,
    "label": {
        "normal": {
            "show": True,
            "position": "insideBottom",
            "align": "center",
            "textBorderWidth": 2,
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 4]
                # "formatter": "{b} {c} ( {a} )",
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_bar_stack = {
    "name": "",
    "type": "bar",
    "barMaxWidth": "100",
    "animation": False,
    "stack": "stack",
    "label": {
        "normal": {
            "show": True,
            "position": "insideBottom",
            "align": "center",
            "textBorderWidth": 2,
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 4]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_bar_stack_percent = {
    "name": "",
    "type": "bar",
    "barMaxWidth": "100",
    "animation": False,
    "stack": "stack",
    "label": {
        "normal": {
            "show": True,
            "position": "insideBottom",
            "align": "center",
            "textBorderWidth": 2,
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 10]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_hbar = {
    "name": "",
    "type": "bar",
    "barMaxWidth": "100",
    "barGap": "10%",
    "animation": False,
    "label": {
        "normal": {
            "show": True,
            "position": "insideLeft",
            "formatter": "{a}: {c}",
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 10]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_hbar_stack = {
    "name": "",
    "type": "bar",
    "barMaxWidth": "100",
    "animation": False,
    "stack": "stack",
    "label": {
        "normal": {
            "show": True,
            "position": "insideLeft",
            "formatter": "{a}: {c}",
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 10]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_hbar_stack_percent = {
    "name": "",
    "type": "bar",
    "barMaxWidth": "100",
    "animation": False,
    "stack": "stack",
    "label": {
        "normal": {
            "show": True,
            "position": "insideLeft",
            "formatter": "{a}: {c}",
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 10]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_barline = base_serie_option_bar

base_serie_option_barline_stack = base_serie_option_bar_stack

base_serie_option_barline_line = {
    "name": "",
    "type": "line",
    "symbol": "emptyCircle",
    "showSymbol": False,
    "showAllSymbol": True,
    "smooth": False,
    "animation": False,
    "yAxisIndex": 1,
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "label": {
        "normal": {
            "formatter": "{a}: {c}",
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 10]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_line = {
    "name": "",
    "type": "line",
    "symbol": "emptyCircle",
    "showSymbol": False,
    "showAllSymbol": True,
    "smooth": False,
    "animation": False,
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "label": {
        "normal": {
            "formatter": "{a}: {c}",
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 10]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_line_shadow = {
    "name": "",
    "type": "line",
    "symbol": "emptyCircle",
    "showSymbol": False,
    "showAllSymbol": True,
    "smooth": False,
    "animation": False,
    "areaStyle": {
        "normal": {
            "opacity": 0.4
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "label": {
        "normal": {
            "formatter": "{a}: {c}",
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 10]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_line_stack = {
    "name": "",
    "type": "line",
    "symbol": "emptyCircle",
    "showSymbol": False,
    "showAllSymbol": True,
    "smooth": False,
    "animation": False,
    "stack": "stack",
    "areaStyle": {
        "normal": {
            "opacity": 0.4
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        }
    },
    "label": {
        "normal": {
            "formatter": "{a}: {c}",
        }
    },
    "markLine": {
        "data": [],
        "label": {
            "normal": {
                "position": "left",
                "show": True,
                "formatter": "{c}",
                "fontStyle": 'normal',
                "fontSize": 12,
                "padding": [4, 10]
            }
        },
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_pie = {
    "name": "",
    "data": [],
    "type": "pie",
    "radius": "55%",
    "center": ["50%", "60%"],
    "label": {
        "normal": {
            "formatter": "{c} ({d} %)"
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        },
        "emphasis": {
            "shadowBlur": 10,
            "shadowOffsetX": 0,
            "shadowColor": "rgba(0, 0, 0, 0.5)"
        }
    },
    "labelLine": {
        "normal": {
            "show": True,
            "length": 10,
            "length2": 7
        }
    },
    "animation": True,
    "z": 2,
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_radar = {
    "name": "",
    "type": "radar",
    "data": [],
    "animation": False,
    "symbol": "none",
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_map = {
    "name": "",
    "type": "map",
    "mapType": "china",
    "selectedMode": "multiple",
    "roam": False,
    "showLegendSymbol": False,
    "label": {
        "normal": {
            "show": False,
            "formatter": None
        },
        "emphasis": {
            "show": False
        }
    },
    "itemStyle": {
        "emphasis": {
            "areaColor": "#1B74CF",
        }
    },
    "top": 0,
    "bottom": 0,
    "data": [],
    "tooltip": {
        "formatter": None
    },
    "field_id": None,
    "id": None
}

bak_base_serie_option_gauge = {
    "type": "gauge",
    "startAngle": 220,
    "endAngle": -40,
    "min": 0,
    "max": 200,
    "precision": 0,
    "splitNumber": 4,
    "axisLine": {
        "show": True,
        "lineStyle": {
            "color": [[0, "#53a4f4"], [1, "#53a4f4"]],
            "width": 30
        }
    },
    "axisTick": {
        "show": True,
        "splitNumber": 10,
        "length": 8,
        "lineStyle": {
            "color": "#eee",
            "width": 1,
            "type": "solid"
        }
    },
    "axisLabel": {
        "show": True,
        "textStyle": {
            "color": "#333",
            "fontSize": 16
        }
    },
    "splitLine": {
        "show": True,
        "length": 30,
        "lineStyle": {
            "color": "#eee",
            "width": 2,
            "type": "solid"
        }
    },
    "pointer": {
        "length": "80%",
        "width": 8,
        "color": "#506078"
    },
    "title": {
        "show": True,
        "offsetCenter": ["0%", 130],
        "textStyle": {
            "color": "#616161",
            "fontSize": 20
        }
    },
    "detail": {
        "show": True,
        "backgroundColor": "rgba(0,0,0,0)",
        "offsetCenter": ["0%", 70],
        "textStyle": {
            "color": "#484848",
            "fontSize": 60,
            "fontWeight": "bold"
        }
    },
    "data": [],
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_gauge = {
    "name": "",
    "data": [],
    "tooltip": {
        "formatter": None
    },
    "label": {
        "normal": {
            "formatter": None
        }
    },
    "field_id": None,
    "id": None
}

base_serie_option_score_card = {
    "name": "",
    "data": [],
    "tooltip": {
        "formatter": None
    },
    "label": {
        "normal": {
            "formatter": None
        }
    },
    "field_id": None,
    "id": None
}

base_serie_option_submitrate = {
    "name": "",
    "data": [],
    "tooltip": {
        "formatter": None
    },
    "label": {
        "normal": {
            "formatter": None
        }
    },
    "field_id": None,
    "id": None
}

base_serie_option_scatter = {
    "name": "",
    "type": "scatter",
    "symbolSize": "$$self.sizeFunc$$",
    "label": {
        "emphasis": {
            "show": True,
            "formatter": "$$self.formatterFunc$$",
            "position": "top"
        }
    },
    "itemStyle": {
        "normal": {
            "shadowBlur": 10,
            "shadowColor": "rgba(120, 36, 50, 0.5)",
            "shadowOffsetY": 5,
        }
    },
    "animation": False,
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_treemap = {
    "name": "矩形图",
    "type": "treemap",
    "itemStyle": {
        "normal": {
            "color": None,
            "label": {
                "show": True,
                "formatter": "{b}"
            },
            "borderWidth": 1
        },
        "emphasis": {
            "label": {
                "show": True
            }
        }
    },
    "data": [],
    "animation": False,
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_grid_bar = {
    "name": "",
    "type": "bar",
    "barMaxWidth": "100",
    "barGap": "10%",
    "label": {
        "normal": {
            "show": True,
            "position": "insideBottom",
            "align": "center",
            "textBorderWidth": 2,
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        },
    },
    "animation": False,
    "xAxisIndex": 1,
    "yAxisIndex": 1,
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_grid_hbar = {
    "name": "",
    "type": "bar",
    "barMaxWidth": "100",
    "barGap": "10%",
    "label": {
        "normal": {
            "show": True,
            "position": "insideLeft",
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        },
    },
    "animation": False,
    "xAxisIndex": 1,
    "yAxisIndex": 1,
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_grid_line = {
    "name": "",
    "type": "line",
    "barMaxWidth": "100",
    "label": {
        "normal": {
            "show": True,
            "position": "top"
        }
    },
    "itemStyle": {
        "normal": {
            "color": None,
        },
    },
    "animation": False,
    "xAxisIndex": 1,
    "yAxisIndex": 1,
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_tag = {
    "name": "",
    "type": "custom",
    "itemStyle": {
        "normal": {
            "color": None,
        },
    },
    "label": {
        "normal": {
            "show": False,
            "formatter": None
        }
    },
    "tooltip": {},
    "field_id": None,
    "id": None
}

base_serie_option_index_card = {}
base_serie_option_dict[field_consts.FIELD_TTYPE_BAR] = base_serie_option_bar
base_serie_option_dict[field_consts.FIELD_TTYPE_BAR_STACK] = base_serie_option_bar_stack
base_serie_option_dict[field_consts.FIELD_TTYPE_BAR_STACK_PERCENT] = base_serie_option_bar_stack_percent
base_serie_option_dict[field_consts.FIELD_TTYPE_HBAR] = base_serie_option_hbar
base_serie_option_dict[field_consts.FIELD_TTYPE_HBAR_STACK] = base_serie_option_hbar_stack
base_serie_option_dict[field_consts.FIELD_TTYPE_HBAR_STACK_PERCENT] = base_serie_option_hbar_stack_percent
base_serie_option_dict[field_consts.FIELD_TTYPE_BARLINE] = base_serie_option_barline
base_serie_option_dict[field_consts.FIELD_TTYPE_BARLINE_STACK] = base_serie_option_barline_stack
base_serie_option_dict[field_consts.FIELD_TTYPE_LINE] = base_serie_option_line
base_serie_option_dict[field_consts.FIELD_TTYPE_LINE_SHADOW] = base_serie_option_line_shadow
base_serie_option_dict[field_consts.FIELD_TTYPE_LINE_STACK] = base_serie_option_line_stack
base_serie_option_dict[field_consts.FIELD_TTYPE_PIE] = base_serie_option_pie
base_serie_option_dict[field_consts.FIELD_TTYPE_MAP] = base_serie_option_map
base_serie_option_dict[field_consts.FIELD_TTYPE_GAUGE] = base_serie_option_gauge
base_serie_option_dict[field_consts.FIELD_TTYPE_SCORE_CARD] = base_serie_option_score_card
base_serie_option_dict[field_consts.FIELD_TTYPE_RADAR] = base_serie_option_radar
base_serie_option_dict[field_consts.FIELD_TTYPE_SCATTER] = base_serie_option_scatter
base_serie_option_dict[field_consts.FIELD_TTYPE_TREEMAP] = base_serie_option_treemap
base_serie_option_dict[field_consts.FIELD_TTYPE_INDEX_CARD] = base_serie_option_index_card
base_serie_option_dict[field_consts.FIELD_TTYPE_SUBMITRATE] = base_serie_option_submitrate
base_serie_option_dict[field_consts.FIELD_TTYPE_BARLINE_LINE] = base_serie_option_barline_line
base_serie_option_dict[field_consts.FIELD_TTYPE_GRID_BAR] = base_serie_option_grid_bar
base_serie_option_dict[field_consts.FIELD_TTYPE_GRID_HBAR] = base_serie_option_grid_hbar
base_serie_option_dict[field_consts.FIELD_TTYPE_GRID_LINE] = base_serie_option_grid_line
base_serie_option_dict[field_consts.FIELD_TTYPE_TAG] = base_serie_option_tag

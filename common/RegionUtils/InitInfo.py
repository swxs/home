# -*- coding: utf-8 -*-
# @File    : InitInfo.py
# @Time    : 2018/3/21 11:32

import math
import numpy as np
import pandas as pd
from common.RegionUtils import NotExistDealerInfoException, MultiDealerInfoException


class InitInfo(object):
    def __init__(self, filename=None, layer_list=None):
        self.filename = filename
        self.layer_list = layer_list
        self.info_list = list()
        self.create_info_list()

    def __iter__(self):
        return iter(self.info_list)

    def _clear_data(self, value):
        if isinstance(value, (np.int, np.int8, np.int16, np.int32, np.int64, np.long)):
            return int(value)
        elif isinstance(value, (np.float, np.float16, np.float32, np.float64)):
            if math.isnan(value):
                return None
            elif np.isinf(value):
                return None
            else:
                return float(value)
        else:
            return value

    def create_info_list(self):
        layer_df_list = []
        for layer in self.layer_list:
            try:
                df = pd.read_excel(self.filename, layer)
            except Exception as e:
                if layer == self.layer_list[-1]:
                    raise NotExistDealerInfoException()
                print(repr(e))
                continue

            if "门店编码" in df.columns.tolist():
                df["code"] = df["门店编码"]
                del df["门店编码"]

            if "名称" in df.columns.tolist():
                df["name"] = df["名称"]
                del df["名称"]

            if "邮箱" in df.columns.tolist():
                df["email"] = df["邮箱"]
                del df["邮箱"]

            if "联系方式" in df.columns.tolist():
                df["phone"] = df["联系方式"]
                del df["联系方式"]

            if layer == self.layer_list[-1]:
                if "code" not in df.columns.tolist():
                    raise NotExistDealerInfoException()

            df.dropna(subset=["name"], inplace=True)
            multiple_list = list(df["name"][df["name"].duplicated()])
            if len(multiple_list) > 0:
                raise MultiDealerInfoException(multiple_list)
            df.set_index(["name"], inplace=True)
            layer_df_list.append(dict(layer=layer, df=df))

        for layer_df in layer_df_list:
            layer_info = dict()

            data = layer_df.get('df').to_dict()
            for attr, attr_info in data.items():
                for name, value in attr_info.items():
                    if name in layer_info:
                        layer_info[name].update({attr: self._clear_data(value)})
                    else:
                        layer_info[name] = dict(name=name, layer=layer_df.get('layer'))
                        layer_info[name].update({attr: self._clear_data(value)})

            for layer, info in layer_info.items():
                self.info_list.append(info)

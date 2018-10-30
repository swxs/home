# -*- coding: utf-8 -*-
# @File    : save_region_dataframe.py
# @AUTH    : swxs
# @Time    : 2018/9/14 10:50

import os
import sys

if __name__ == '__main__':
    sys.path.insert(0, os.path.abspath(os.curdir))

import json
import yaml
import numpy as np
import pandas as pd
import datetime
import settings
from BaseDocument import BaseDocument
from api.utils.organization.region import Region
from api.utils.organization.region_type import RegionType
from common.Helpers.DBHelper_Redis import RedisDBHelper
redis_helper = RedisDBHelper()

NOT_SET = "none"

DTYPE_MODIFY = {
    NOT_SET: (None, lambda x: x),
    "string": (None, lambda x: x),
    "int": (np.int64, lambda x: int(float(x))),
    "int8": (np.int8, lambda x: int(float(x))),
    "int16": (np.int16, lambda x: int(float(x))),
    "int32": (np.int32, lambda x: int(float(x))),
    "int64": (np.int64, lambda x: int(float(x))),
    "float": (np.float64, lambda x: float(x)),
    "float16": (np.float16, lambda x: float(x)),
    "float32": (np.float32, lambda x: float(x)),
    "float64": (np.float64, lambda x: float(x)),
}


def get_model_value(model, name):
    value = model
    for name_step in name.split("."):
        if isinstance(value, BaseDocument):
            value = value.__getattribute__(name_step)
        else:
            value = value.get(name_step)
    return value


def clear_extra_data_list(extra_data_list):
    cleared_extra_data_list = list()
    for extra_data in extra_data_list:
        name = extra_data.get("name")
        display_name = extra_data.get("display_name", name)
        ttype = extra_data.get("ttype", NOT_SET).lower()
        dtype = extra_data.get("dtype", DTYPE_MODIFY.get(ttype, DTYPE_MODIFY[NOT_SET])[0])
        cleared_extra_data_list.append(dict(
            name=name,
            display_name=display_name,
            ttype=ttype,
            dtype=dtype
        ))
    return cleared_extra_data_list


def get_region_name(region, extra_data_list=None):
    info_list = []
    current_region = region
    while 1:
        if current_region.parent_id is None:
            break
        else:
            info_list.append(current_region.region_code)
            current_region = Region.get_region_by_region_id(current_region.parent_id)
    for data in extra_data_list:
        value = get_model_value(region, data.get('name'))
        ttype = data.get("ttype", NOT_SET)
        info_list.append(DTYPE_MODIFY.get(ttype, DTYPE_MODIFY[NOT_SET])[1](value))
    return info_list

def update_project_region_code(project_id):
    region_list = Region.get_region_list_by_project_id(project_id)
    for region in region_list:
        region_code = redis_helper.get_next_seq(f"region_{region.ttype}")
        region.update(region_code=int(region_code))

def save_project_region_dataframe(project_id, clear_test=False):
    output_filename = f"region_{project_id}.h5"
    output_filepath = os.path.join(settings.DATA_FILE_PATH, output_filename)

    cleared_extra_data_list = [
        {"name": "name", "display_name": "名称"},
        {"name": "code", "display_name": "编号"},
    ]

    region_list = Region.get_dealer_region_list_by_project_id(project_id)
    if clear_test:
        # MCD特色， 当时存在一个有问题的test dealer
        region_list = [region for region in region_list if region.parent_id is not None]

    info_list = [get_region_name(region, cleared_extra_data_list) for region in region_list]
    new_info_list = list(map(list, zip(*info_list)))

    region_type_display_name_list = [region_type.display_name for region_type in RegionType.get_region_type_list_by_project_id(project_id)][1:]
    region_type_display_name_list.reverse()

    #  这里可以优化下
    data = dict()
    dtype = dict()
    df_index = list()

    current_index = 0
    for index, display_name in enumerate(region_type_display_name_list):
        current_index = index
        data[display_name] = new_info_list[current_index]
        dtype[display_name] = np.int32
        df_index.append(display_name)
    for i, extra_data in enumerate(cleared_extra_data_list, start=(current_index + 1)):
        data[extra_data.get("display_name")] = new_info_list[i]
        if extra_data.get("dtype") is not None:
            dtype[extra_data.get("display_name")] = extra_data.get("dtype")
        df_index.append(extra_data.get("display_name"))

    pd.DataFrame(data=data).astype(dtype=dtype).reindex(columns=df_index).to_hdf(output_filepath, key="table", mode="w")

    return output_filename


if __name__ == "__main__":
    save_project_region_dataframe("5b99caa6c332011cf874474c")
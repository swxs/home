# -*- coding: utf-8 -*-
# @File    : clear_redis_dbcache.py
# @AUTH    : swxs
# @Time    : 2019/5/8 16:41

from common.Helpers.DBHelper_Redis import redis_helper


if __name__ == "__main__":
    # 清除所有缓存
    redis_helper.run_script(
        "SCAN_DEL_WITH_PREFIXLUA",
        [
            "IBF*",
        ],
        [],
    )

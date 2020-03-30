# -*- coding: utf-8 -*-
# @File    : daterange_utils.py
# @AUTH    : swxs
# @Time    : 2019/2/27 16:07

import time
import datetime
import calendar
import arrow
import settings
from functools import wraps

DAY_OF_WEEKDAY = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

MON_SUN = 1
SUN_SAT = 2
WEEK_TYPE_LIST = [
    (MON_SUN, '周一至周日'),
    (SUN_SAT, '周日至周六'),
]

NEAR_HALF_YEAR = 1
FRONT_HALF_YEAR = 2
BEHAND_HALF_YEAR = 3
HALF_YEAR_TYPE_LIST = [
    (NEAR_HALF_YEAR, '最近半年'),
    (FRONT_HALF_YEAR, '上半年'),
    (BEHAND_HALF_YEAR, '下半年')
]


def convert_date_to_datetime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return datetime.datetime.combine(func(*args, **kwargs), datetime.time(0, 0, 0))

    return wrapper


def get_weekday(x):
    return DAY_OF_WEEKDAY[x]


def get_today(base=arrow.utcnow()):
    return get_shift_day(0, base=base)


def get_yesterday(base=arrow.utcnow()):
    return get_shift_day(-1, base=base)


def get_shift_day(n, base=arrow.utcnow()):
    return arrow.get(base).shift(days=n).date()


def get_current_week(base=arrow.utcnow()):
    return get_shift_week(0, base=base)


def get_last_week(base=arrow.utcnow()):
    return get_shift_week(-1, base=base)


def get_shift_week(n, base=arrow.utcnow()):
    return arrow.get(base).shift(days=-arrow.get(base).weekday()).shift(weeks=n).date()


def get_current_month(base=arrow.utcnow()):
    return get_shift_month(0, base=base)


def get_last_month(base=arrow.utcnow()):
    return get_shift_month(-1, base=base)


def get_shift_month(n, base=arrow.utcnow()):
    return arrow.get(base).replace(day=1).shift(months=n).date()


def get_current_quarter(base=arrow.utcnow()):
    return get_shift_quarter(0, base=base)


def get_last_quarter(base=arrow.utcnow()):
    return get_shift_quarter(-1, base=base)


def get_shift_quarter(n, base=arrow.utcnow()):
    return arrow.get(base).replace(month=(((arrow.get(base).month + 2) // 3 - 1) * 3 + 1), day=1).shift(quarters=n).date()


def get_current_year(base=arrow.utcnow()):
    return get_shift_year(0, base=base)


def get_last_year(base=arrow.utcnow()):
    return get_shift_year(-1, base=base)


def get_shift_year(n, base=arrow.utcnow()):
    return arrow.get(base).replace(month=1, day=1).replace(years=n).date()


def get_day_number_of_month(date):
    return date.timetuple().tm_mday


def get_day_number_of_year(date):
    return date.timetuple().tm_yday


def get_weekday_of_day(date):
    return date.weekday()


def get_day_of_month(date):
    return calendar.monthrange(date.year, date.month)[1]


def get_timestamp_start(days_before):
    return int(time.time()) - 60 * 60 * 24 * days_before


def is_leap(year):
    return ((year % 4 == 0) and (year % 100 != 0)) or ((year % 100 == 0) and (year % 400 == 0))


def get_timestamp(base):
    if base is None:
        base = arrow.utcnow()
    return arrow.get(base).timestamp


@convert_date_to_datetime
def shift_month_begin(n, base=None):
    if base is None:
        base = arrow.utcnow()
    return arrow.get(base).shift(months=n).replace(day=1).date()


@convert_date_to_datetime
def shift_day(n, base=None):
    if base is None:
        base = arrow.utcnow()
    return arrow.get(base).shift(days=n).date()


if __name__ == "__main__":
    print(get_timestamp(shift_day(1, base="2019-04-03 00:01:12")))

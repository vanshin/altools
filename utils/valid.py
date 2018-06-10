# encoding:utf-8

'''valid from qf'''

import time
import json
import datetime

from functools import partial

from .constants import DATETIME_FMT

def is_valid(s, func):
    try:
        func(s)
        return True
    except:
        return False

# 判断是否是日期
is_valid_date = partial(is_valid, func=lambda s: time.strptime(s, DATE_FMT))

# 判断是否是时间
is_valid_datetime = partial(is_valid, func=lambda s: time.strptime(s, DATETIME_FMT))

# 判断是否是数字
is_valid_num= partial(is_valid, func=float)

# 判断是否是整形
is_valid_int= partial(is_valid, func=int)

# 判断是否能json.dumps
is_valid_json= partial(is_valid, func=json.dumps)

is_valid_str = partial(is_valid, func=str)

# 判断是否datetime
def is_date_type(v):
    return isinstance(v, (datetime.date, datetime.time))







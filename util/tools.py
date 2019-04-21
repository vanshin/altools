'''tools set'''

import random
import string

from .runtime import hids
from .valid import is_valid_int
from ..base.error import ToolExcp

def random_str(length=4):

    a = []

    for i in range(length):
        a.append(random.choice(string.ascii_lowercase))
    return ''.join(a)

def encode_id(t):
    if not is_valid_int(t):
        raise ParamExcp('加密函数参数错误')
    try:
        result = hids.encode(int(t))
        return result
    except:
        raise ToolExcp('加密错误')

def decode_id(t, default=None):
    try:
        result = hids.decode(t)
        if not result and default:
            return default
        if len(result) == 1:
            return result[0]
        else:
            return result
    except:
        raise ToolExcp('解压失败')

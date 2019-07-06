'''tools set'''

import random
import string
import hashlib

from .runtime import hids
from .valid import is_valid_int
from ..base.error import ToolExcp

def random_str(length=4):

    a = []
    for i in range(length):
        a.append(random.choice(string.ascii_lowercase))
    return ''.join(a)

def encry_str(raw_str):

    left_salt = random_str()
    right_salt = random_str()
    salted_str = left_salt + raw_str + right_salt
    encryed_str = hashlib.sha256(salted_str)
    return f'{left_salt}@{encryed_str}@{right_salt}'

def check_pass(passwd, encryed_passws) -> bool:

    left, en, right = encryed_passws.split('@')
    salted = left + passwd + right
    encryed_str = hashlib.sha256(salted)

    if encryed_str == encryed_passws:
        return True
    return False

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

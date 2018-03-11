#coding=utf-8
import json
import datetime
import config

from flask import jsonify
from flask import request

class RRET:
    SUCCESS = 2000
    USER_NOT_LOGIN = 4041
    USER_NOT_EXIST = 4042
    RES_NOT_EXIST = 4043
    USER_NOT_SELF = 4044
    PARAM_ERROR = 5001


MES = {
    2000: 'SUCCESS',
    4041: 'USER_NOT_LOGIN',
    4042: 'USER_NOT_EXIST',
    4043: 'RES_NOT_EXIST',
    5001: 'PARAM_ERROR',
}

def json_default_trans(obj):
    '''json对处理不了的格式的处理方法'''
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError('%r is not JSON serializable' % obj)



def output(code=0000, message='success', data=None):
    ret = {
        'code': code,
        'message': message,
        'data': {}
    }
    if not data:
        return jsonify(ret)
    ret['data'] = data

    return jsonify(ret)


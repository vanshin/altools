
import json
import datetime


def json_default_trans(obj):
    '''json对处理不了的格式的处理方法'''
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')
    raise TypeError('%r is not JSON serializable' % obj)



def output(data=None, code='2000', message='SUCCESS'):

    ret = {
        'code': code,
        'message': message,
        'data': '' if data is None else data
    }

    return json.dumps(ret, default=json_default_trans)


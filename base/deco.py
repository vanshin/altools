#coding=utf8

import logging
log = logging.getLogger()

from functools import wraps

def show_args(func):
    @wraps(func)
    def _(*args, **kwargs):
        log_list = []
        log_temp = '{}={}'
        count = 1
        for i in args:
            log_list.append(log_temp.format('arg_'+str(count), i))
            count += 1
        for k,v in kwargs:
            log_list.append(log_temp.format(k,v))
        log_str = '|'.join(log_list)
        log.info(log_str)
        return func(*args, **kwargs)
    return _

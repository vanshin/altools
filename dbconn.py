#coding=utf-8

'''db connection class'''

import pymyql

__pool = None

def create_pool(**kw):
    '''create dbpool'''
    log.info('creating dbpool')
    global __pool
    __pool = pymysql.connect(
        host = kw.get('host', '127.0.0.1'),
        port = kw.get('post', 3306),
        user = kw.get('user'),
        password = kw.get('password'),
        db = kw.get('db'),
        charset = kw.get('charset', 'utf8'),
        autocommit = kw.get('autocommit', True),
        # maxsize = kw.get('maxsize', 10),
        # minsize = kw.get('minsize', 1),
    )

class DBConn(object):
    '''dbconn class'''

    def __init__(self, ):
        self.dbconf =

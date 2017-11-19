#coding=utf-8

'''db connection class'''

import pymysql
import logging
import queue
log = logging.getLogger()

from tools import Pool

__pool = None

def init_pool(dbsconf):
    global __pool
    if __pool:
        log.warn('dbpool is existed')
        return __pool
    __pool = DBPool(dbsconf)
    return __pool

class DBPool(object):

    def __init__(self, dbconfs):

        global __pool
        __pool = {}

        self.dbconfs = dbconfs
        for k,v in dbconfs.items():
            max_size = v.get('max_size', 10)
            pool = Pool(max_size)
            for i in range(max_size):
                conn = DBConn(v)
                pool.put(conn)
            __pool[k] = pool

    def get(self, name):
        global __pool
        return __pool[name]


class DBConnBase(object):
    def __init__(self):
        pass

class DBConn(DBConnBase):
    '''dbconn class'''

    def __init__(self, dbconf):
        self.dbconf = dbconf
        self.conn = pymysql.connect(
            host = dbconf.get('host', '127.0.0.1'),
            port = dbconf.get('post', 3306),
            user = dbconf.get('user'),
            password = dbconf.get('password'),
            db = dbconf.get('db'),
            charset = dbconf.get('charset', 'utf8'),
            autocommit = dbconf.get('autocommit', True),
            )

    def get_conn(self):
        pass

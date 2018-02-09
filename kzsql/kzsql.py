#coding=utf8

'''main page'''

import logging
log = logging.getLogger()

from dbconn import DBPool, init_pool

def init_kzsql(dbsconf):
    dbconns = init_pool(dbsconf)
    if dbconns:
       log.info('init {}'.format(','.join([k for k in dbsconf])))

    return dbconns


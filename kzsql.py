#coding=utf8

'''main page'''

import logging
log = logging.getLogger()

from dbconn import DBPool, init_pool

def init_kzsql(dbsconf):
    if init_pool(dbsconf):
       log.info('init {}'.format(','.join([k for k in dbsconf])))



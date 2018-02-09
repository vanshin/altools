#coding=utf8

'''redis cli and other'''

import redis
import config
import sqlalchemy

from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine(config.dbconf, echo=False)
Session = sessionmaker(bind=engine)

dbsess = Session()
kotori = redis.Redis(**config.KOTORI_REDIS_CONF)

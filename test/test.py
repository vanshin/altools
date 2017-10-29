import sys

sys.path.append('/home/vanshin/code/basicframe')

from kzsql import init_kzsql
from dbmodel import Model
from field import *

dbsconf = {
    'rd_user': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'rd_user',
    },
    'rd_user': {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
        'db': 'rd_user',
    }
}

sql = init_kzsql(dbsconf)

class User(Model):
    '''test user'''
    __tablename__ = 'auth_user'

    id = IntegerField(primary_key=True)
    name = StringField()
    age = IntegerField()
    sex = IntegerField()

us = User()
ret = us.find_all()
print(ret)



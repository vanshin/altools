from aiopeewee import AioModel, AioMySQLDatabase

from peewee import CharField, IntegerField, DatetimeField

from dbs import db_basic

class User(AioModel):

    id = IntegerField(primary_key=True)
    username = CharField(max_length=32)
    type = IntegerField()
    status = IntegerField()
    email = CharField(max_length=64)
    mobile = CharField(max_length=15)
    password = CharField(max_length=1024)
    login_ip = CharField(max_length=64)
    create_time = DatetimeField()
    update_time = DatetimeField()


    class Meta:
        database = db_basic


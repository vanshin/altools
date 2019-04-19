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

    async def add_user(self, **kw):

        args_idft = {
            'int': ['type', 'status'],
            'str': [
                'username', 'email', 'mobile', 'password',
                'login_ip',
            ],
            'datetime': ['create_time', 'update_time']
        }

        v = build_args(args_idft, kw)

        await db_basic.connect()
        await self.create()



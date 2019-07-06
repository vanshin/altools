'''user model link basic db'''


from peewee import CharField, IntegerField, DateTimeField
from peewee import IntegrityError, DoesNotExist

from aiopeewee import AioModel

from .dbs import db_basic

from ..excepts import ServerError
from ..util.tools import encry_str

class User(AioModel):

    class Meta:
        database = db_basic

    id = IntegerField(primary_key=True)
    username = CharField(max_length=32)
    type = IntegerField()
    status = IntegerField()
    email = CharField(max_length=64)
    mobile = CharField(max_length=15)
    password = CharField(max_length=1024)
    login_ip = CharField(max_length=64)
    create_time = DateTimeField()
    update_time = DateTimeField()

    @classmethod
    async def add_user(cls,
        username:str, email:str, mobile:str, password:str,
        login_ip:str, type:int, status:int,
    ) -> int:

        await db_basic.connect()

        row = None

        try:
            row = await cls.create(
                username=username, email=email, mobile=mobile,
                password=encry_str(password),
                login_ip=login_ip, type=type
            )
        except IntegrityError as e:
            raise ServerError(e.args[1])

        return row

    async def check_user_exist(self, username:str, password:str
    ) -> bool:

        await db_basic.connect()

        try:
            user = self.get(User.username = username)
        except DoesNotExist as e:
            raise


    async def check_user_pass(self, username:str, password:str
    ) -> bool:

        await db_basic.connect()



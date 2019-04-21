
import inspect
import functools
import collections

from .excepts import ServerError

from aiopeewee import AioModel

from peewee import CharField, IntegerField, DateTimeField
from peewee import IntegrityError

from .dbs import db_basic


class TypeCheckMeta(type):

    @staticmethod
    def check(func):
        msg = ('Expected type {expected!r} for argument {argument}, '
               'but got type {got!r} with value {value!r}')
        # 获取函数定义的参数
        sig = inspect.signature(func)
        parameters = sig.parameters          # 参数有序字典
        arg_keys = tuple(parameters.keys())   # 参数名称
        ret_anon = sig.return_annotation

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            CheckItem = collections.namedtuple('CheckItem', ('anno', 'arg_name', 'value'))
            check_list = []

            # collect args   *args 传入的参数以及对应的函数参数注解
            for i, value in enumerate(args):
                arg_name = arg_keys[i]
                anno = parameters[arg_name].annotation
                check_list.append(CheckItem(anno, arg_name, value))

            # collect kwargs  **kwargs 传入的参数以及对应的函数参数注解
            for arg_name, value in kwargs.items():
               anno = parameters[arg_name].annotation
               check_list.append(CheckItem(anno, arg_name, value))

            # check type
            for item in check_list:
                if not isinstance(item.value, item.anno):
                    error = msg.format(expected=item.anno, argument=item.arg_name,
                                       got=type(item.value), value=item.value)
                    raise TypeError(error)

            ret = func(*args, **kwargs)
            if not  isinstance(ret, ret_anon):
                raise TypeError(f'{type(ret) is not {ret_anon}}')
            return ret

        return wrapper

    def __new__(cls, name, bases, attrs):
        checked_funcs = getattr(cls, 'check', [])
        for k,v in attrs.items():
            if k in checked_funcs:
                v = cls.check(v)
        return type.__new__(cls, name, bases, attrs)

# class User(object):

    # id: int
    # username: str
    # type: int
    # status: int
    # email: str
    # mobile: str
    # password: str
    # login_ip: str
    # create_time: datetime.datetime
    # update_time: datetime.datetime


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
                password=password, login_ip=login_ip, type=type
            )
        except IntegrityError as e:
            raise ServerError(e.args[1])

        return row

    def


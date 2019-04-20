'''basic api handler'''

import traceback

from quart import request
from quart.views import MethodView, MethodViewType

from .builder.args_builder import ArgsBuilder
from .excepts import ParamError, BaseError
from .output import output

class CheckAllMeta(MethodViewType):

    @staticmethod
    def check(func):
        async def _(self, *args, **kw):
            try:
                return await func(self, *args, **kw)
            except BaseError as e:
                print(traceback.format_exc())
                return output(code=e.code, message=e.message)
        return _

    def __new__(cls, name, bases, attrs):

        checked_funcs = ['get', 'post', 'put']

        for k,v in attrs.items():
            if k in checked_funcs:
                attrs[k] = cls.check(v)
        return type.__new__(cls, name, bases, attrs)


class BaseView(MethodView, metaclass=CheckAllMeta):

    _dofors = ('all', 'existence', 'page')
    _dtype = ('form', 'json')

    def __init__(self):
        self.args_builder = getattr(self, 'args_builder', ArgsBuilder)
        self.args_idft= {}
        self.args_lang_map = {}
        self.required_args = set()
        request_context = ['remote_addr', ]
        for i in request_context:
            v = getattr(request, i, None)
            setattr(self, i, v)

    # def __getattr__(self, name):
        # if hasattr(request, name):
            # return getattr(request, name)
        # raise AttributeError

    async def source_by_dtype(self, dtype):
        '''获取初始数据'''

        if hasattr(self, 'source_data'):
            return self.source_data

        self.source_data = {}
        if dtype == 'form':
            self.source_data = request.args or await request.form
        elif dtype == 'json':
            self.source_data = await request.get_data
        print(f'source data {self.source_data}')

    async def build_args(self, dtype='form', dofor='all'):
        '''验证参数

        params:
            dtype(str): 如何获取前端的数据 (json, form)
            dofor(str): 如何生成参数 (all, existence, ……)
        return:
            args: 返回指定类型的参数

        all:
            验证所有的参数(除了manual)符合指定类型并且存在, 默认模式
        existence:
            验证存在的参数,符合指定类型. 用在分页查询等接口
        page:
            分页数据，自动从参数中寻找分页控制参数

        '''

        if dofor not in self._dofors:
            # log.warn('MH> not support dofor {}'.format(dofor))
            raise ParamError('内部错误')
        if dtype not in self._dtype:
            # log.warn('MH> not support dtype {}'.format(dtype))
            raise ParamError('内部错误')

        if hasattr(self, 'values') and self.values:
            return self.values

        # log.info('MH> args_builder == {}'.format(self.args_builder.__name__))

        # 初始化数据
        await self.source_by_dtype(dtype)
        # 生成args builder实例并执行build
        self._aber= self.args_builder(
            self.args_idft, self.source_data, dofor,
        )
        if self.required_args:
            self._aber.set_required_args(self.required_args)
        self._aber.build()

        # 生成的数据
        self.values = self._aber.values
        self.others = self._aber.others
        self.source = self._aber.source
        # log.info('MH> built_source == {}'.format(self.source))
        # log.info('MH> built_args == {}'.format(self.values))
        # log.info('MH> built_others == {}'.format(self.others))
        return self.values

    def require(self, *args):
        for arg in args:
            self.required_args.add(arg)


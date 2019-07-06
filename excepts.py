import define


class BaseError(Exception):

    def __init__(self, code, msg):
        self.code = code
        self.message = msg

class NotExistError(BaseError):

    def __init__(self, msg=None):
        self.code = define.ErrorCodeDef.NOT_EXIST
        self.message = msg or define.ErrorCodeDef.MAP[self.code]

class InnerError(BaseError):

    def __init__(self, msg=None):
        self.code = define.ErrorCodeDef.INNER_ERROR
        self.message = msg or define.ErrorCodeDef.MAP[self.code]


class ParamError(InnerError):

    def __init__(self, msg='参数错误'):
        InnerError.__init__(self, msg)

class ServerError(InnerError):

    def __init__(self, msg='服务错误'):
        InnerError.__init__(self, msg)

class UserNotExit(NotExistError):

    def __init__(self, msg='此用户不存在'):
        NotExistError.__init__(self, msg)

class PassNotCorrect(InnerError):

    def __init__(self, msg='密码错误'):
        InnerError.__init__(self, msg)

class ParamNotExist(self):

    def __init__(self, msg='参数不存在'):
        NotExistError.__init__(self, msg)


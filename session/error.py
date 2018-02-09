#coding=utf8

'''error code'''

from .output import output, RRET


class BaseException(Exception):

    def __init__(self, message='', code=RRET.SUCCESS):
        super(BaseException, self).__init__(message, code)
        self.message = message
        self.code = code


class ParamExcp(BaseException):
    def __init__(self, message='参数错误', code=RRET.PARAM_ERROR):
        super(ParamExcp, self).__init__(message, code)

class UserExcp(BaseException):
    def __init__(self, message='用户不存在', code=RRET.USER_NOT_EXIST):
        super(ParamExcp, self).__init__(message, code)



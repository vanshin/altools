#coding=utf8

'''处理session相关'''

from model.user import User

from .tools import get_uuid
from .runtime import kotori, dbsess
from .error import ParamExcp, UserExcp
from .constants import SESSION_KEY


class LoginUser():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.info = {
            'username': self.username,
            'password': self.password
        }
        self.status = 0

    def __getattr__(self, item):
        if item in self.info:
            return self.info[item]
        return None

    def is_login(self):
        '''是否登录'''
        ret = False
        if self.status == 2:
            ret = True
        return ret

    def logout(self, session_id):
        '''删除session'''
        return kotori.delete(session_id)

    def check_user(self):
        '''检查用户是否存在和密码'''
        searched_user = dbsess.query(User).filter(User.username==self.username, User.password==self.password).one()
        self.status = 1
        if not searched_user:
            self.status = -1
            return False
        return True

    def login(self, **kwargs):
        '''登录'''

        if self.status != 1:
            raise UserExcp()

        kwargs['username'] = self.username
        kwargs['password'] = self.password

        self.session_id = get_uuid()
        kotori.hmset(self.session_id, kwargs)
        self.status = 2
        for k,v in kwargs.items():
            self.info[k] = v


        return self.session_id



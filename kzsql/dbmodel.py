#coding=utf-8

'''db model class'''

import logging
import traceback
import time
log = logging.getLogger()

from utils.tools import format_ct
from dbconn import DBPool
from field import *


class DBSession(object):
    def __init__(self, pool, name):
        self.conn = pool.get(name).get()
        self.cursor = self.conn.conn.cursor()

    def db_log(self, info):
        '''print sql log'''
        sql_template = '{time}:|{info}:'
        # log.info(sql_template.format(format_ct(), info))

    def make_args(self, number):
        '''make args string'''

        args = list(number * '?')
        return ','.join(args)

    def select(self, sql, args, size=None, isdict=True, head=False):
        '''select'''

        self.db_log(sql)

        res = None
        ret = []

        self.cursor.execute(sql.replace('?', '%s'), args or ())
        if size:
            res = self.cursor.fetchmany(size)
        else:
            res = self.cursor.fetchall()
        if res and isdict:
            desc_info = self.cursor.description
            field_name = (x[0] for x in desc_info)
            for item in res:
                ret.append(dict(zip(field_name, item)))
        else:
            ret = res
            if head:
                field_name = (x[0] for x in desc_info)
                ret.insert(0, field_name)

        self.db_log(ret)

        if not ret:
            log.info('exec {sql} do not return'.format(sql))
        return ret

    def execute(self, sql, args, atc=True):
        '''for insert, update and delete'''

        self.db_log(log)
        ret = None

        try:
            self.cursor.execute(sql, args)
            affected_num = self.conn.rowcount
        except Exception as e:
            log.warn(traceback.format_exc())
        return affected_num
def make_args(number):
    '''make args string'''

    args = list(number * '?')
    return ','.join(args)

class ModelMetaclass(type):
    '''metaclass for model'''

    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        fields = []
        primary_key = None
        mappings = {}

        tablename = attrs.get('__tablename__', name)
        dbname = attrs.get('__dbname__')
        if not dbname:
            raise ValueError('not found __dbname__')
        log.info('model:{name}|table:{tablename}'.format(name=name, tablename=tablename))

        for k,v in attrs.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.primary_key:
                    if primary_key:
                        raise StandardError('duplicate primary key for table {}'.format(tablename))
                    primary_key = k
                else:
                    fields.append(k)
        if not primary_key:
            raise StandardError('table {} primary key not found'.format(tablename))

        for k in mappings:
            attrs.pop(k)

        escaped_fields = list(map(lambda f:"`{}`".format(f), fields))

        attrs['__mappings__'] = mappings
        attrs['__tablename__'] = tablename
        attrs['__dbsess__'] = None
        attrs['__dbname__'] = dbname
        attrs['__primary_key__'] = primary_key
        attrs['__fields__'] = fields
        attrs['__select__'] = 'select `{primary_key}`, {fields} from `{tablename}`'.format(
                primary_key=primary_key,
                fields=', '.join(escaped_fields),
                tablename=tablename
            )
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values(%s)'.format(
                tablename,
                ','.join(escaped_fields), primary_key,
                make_args(len(escaped_fields)+1)
            )
        attrs['__update__'] = 'update `%s` set %s where `%s` = ?'.format(
                tablename,
                ','.join(map(lambda f: '`%s`=?'.format(mappings.get(f).name or f), fields)),
                primary_key)
        attrs['__delete__'] = 'delete from `%s` where `%s` = ?'.format(
                tablename,
                primary_key
                )
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    '''base model'''

    def __init__(self, dbpool, **kw):
        super(Model, self).__init__(**kw)
        self.dbsess = DBSession(dbpool, self.__dbname__)


    def load(self, **kw):
        pass


    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError('Model has no attr {}'.format(key))

    def __setattr__(self, key, value):
        self[key] = value

    def get_value(self, key):
        return getattr(self, key)

    def get_value_or_default(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                log.info('using default value for {field}:{value}'.format(key, str(value)))
                setattr(self, key, value)
        return value

    # @classmethod
    def find_all(self, where=None, args=None, **kw):
        sql = [self.__select__]
        order_by = kw.get('order_by', None)
        limit = kw.get('limit', None)

        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []
        if order_by:
            sql.append('order by')
            sql.append(order_by)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, (tuple, list)):
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('invalid limit value: %s'.format(str(limit)))
        ret = self.dbsess.select(' '.join(sql), args)
        return ret

    def save(self):
        args = list(map(self.get_value_or_default, self.__fields__))
        args.append(self.get_value_or_default(self.__primary_key__))
        rows = self.dbsess.execute(self.__insert__, args)
        if rows != 1:
            db_log('failed to update by pk: affected rows: {}'.format(rows))

    def remove(self):
        args = [self.get_value(self.__primary_key__)]
        rows = self.dess.execute(self.__delete__, args)
        if rows != 1:
            db_log('failed to remove by pkb affected rows: {}'.format(rows))






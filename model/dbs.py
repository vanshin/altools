'''all database conns'''

from aiopeewee import AioMySQLDatabase

db_basic = AioMySQLDatabase('basic', user='op_basic', password='basic_f17aaabc')
db_blog = AioMySQLDatabase('blog', user='op_blog', password='blog_126ac9f6')

global conns

conns = {
    'basic': db_basic,
    'blog': db_blog
}



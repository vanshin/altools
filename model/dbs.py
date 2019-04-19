
db_basic = AioMySQLDatabase('blog', user='op_blog', password='blog_126ac9f6')
db_blog = AioMySQLDatabase('blog', user='op_blog', password='blog_126ac9f6')

global conns

conns = {
    'basic': db_basic,
    'blog': db_blog
}


def conn_(db_name):
    def _
    return _

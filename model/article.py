from aiopeewee import AioModel, AioMySQLDatabase

from peewee import CharField, IntegerField

from dbs import db_blog

class Article(AioModel):

    id = IntegerField(primary_key=True)
    userid = IntegerField()
    title = CharField(max_length=64)
    body = CharField(max_length=2048)

    class Meta:
        database = db_blog


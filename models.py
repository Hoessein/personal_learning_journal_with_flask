import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

from peewee import *

DATABASE = SqliteDatabase('social.db')


class User(UserMixin, Model):
    title = CharField(unique=True)
    date = DateField()
    time_spent = CharField(max_length=100)
    what_i_learned = TextField()
    resources_to_remember = TextField()
    posted_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by =('-posted_at',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    DATABASE.close()

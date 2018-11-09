import datetime

from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

from peewee import *

DATABASE = SqliteDatabase('social.db')


class Post(Model):
    title = CharField(unique=True)
    date = DateField()
    time_spent = CharField(max_length=100)
    what_i_learned = TextField()
    resources_to_remember = TextField()
    posted_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE


class User(UserMixin, Model):
    username = CharField(unique=True)
    password = CharField()
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE

    @classmethod
    def create_user(cls, username, password, admin=False):
        with DATABASE.transaction():
            try:
                cls.create(
                    username=username,
                    password=generate_password_hash(password),
                    is_admin=admin)
            except IntegrityError:
                raise ValueError("Only admin is allowed")

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Post, User], safe=True)
    DATABASE.close()

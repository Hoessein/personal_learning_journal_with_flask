import unittest

from peewee import *

import app
from models import Post, User

MODELS = [User, Post]

TEST_DB = SqliteDatabase(':memory:')
TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
TEST_DB.connect()
TEST_DB.create_tables(MODELS)

USER_DATA = {
    'username': 'Tester',
    'password': 'Password'
}


class UserModelTestCase(unittest.TestCase):
    @staticmethod
    def create_user():
        User.create_user(
            username='Tester',
            password='Password'
        )

    def test_create_user(self):
        with TEST_DB.bind_ctx(MODELS):
            self.create_user()
            self.assertEqual(User.select().count(), 1)
            self.assertNotEqual(
                User.select().get().password,
                'password'
            )


class PostModelTestCase(unittest.TestCase):
    def test_post_creation(self):
        with TEST_DB.bind_ctx(MODELS):
            Post.create(
                title='Test',
                date='2015-09-09',
                time_spent='50 minutes',
                what_i_learned='A lot of stuff',
                resources_to_remember='Revise, alot'
            )

            self.assertEqual(
                Post.select().count(), 1)


class ViewTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()

    def test_good_login(self):
        with TEST_DB.bind_ctx(MODELS):
            UserModelTestCase.create_user()
            rv = self.app.post('/login', data=USER_DATA)
            self.assertEqual(rv.status_code, 302)
            self.assertEqual(rv.location, 'http://localhost/')


if __name__ == '__main__':
    unittest.main()

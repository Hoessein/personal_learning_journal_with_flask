import unittest

from peewee import *

import app
from models import Post, User

MODELS = [User, Post]

TEST_DB = SqliteDatabase(':memory:')

USER_DATA = {
    'username': 'Admin Tester',
    'password': 'Password'
}

FAKE_USER_DATA = {
    'username': 'Admin2 Tester',
    'password': 'Password2'
}


class SetupTearDownMixin:
    @classmethod
    def setUpClass(cls):
        # ------ ADDED THIS -------
        TEST_DB.bind(MODELS, bind_refs=False, bind_backrefs=False)
        TEST_DB.connect()
        TEST_DB.create_tables(MODELS)

        User.create_user(
            username='Admin Tester',
            password='Password',
            admin=True
        )

    @classmethod
    def tearDownClass(cls):
        # ------ ADDED THIS -------
        TEST_DB.drop_tables(MODELS)
        TEST_DB.close()


class UserModelTestCase(SetupTearDownMixin, unittest.TestCase):

    # @staticmethod
    # def create_user():

    #     User.create_user(
    #         username='Tester',
    #         password='Password'
    #     )

    def test_create_user(self):
        self.assertEqual(User.select().count(), 1)
        self.assertNotEqual(
            User.select().get().password,
            'password'
        )


class ViewTestCase(SetupTearDownMixin, unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()

    def test_good_login(self):
        rv = self.app.post('/login', data=USER_DATA)
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, 'http://localhost/')

    def test_bad_login(self):
        rv = self.app.post('/login', data=FAKE_USER_DATA)
        self.assertEqual(rv.status_code, 200)

    # def test_logout(self):
    #     rv = self.app.get('/logout')
    #     self.assertEqual(rv.status_code, 302)
    #     self.assertEqual(rv.location, 'http://localhost/')

    def test_logged_out_menu(self):
        rv = self.app.get('/')
        self.assertIn('log in', rv.get_data(as_text=True).lower())

    def test_logged_in_menu(self):
        rv = self.app.get('/login', data=USER_DATA)
        rv = self.app.get('/')
        self.assertIn('login', rv.get_data(as_text=True).lower())
        self.assertIn('entries', rv.get_data(as_text=True).lower())
        self.assertIn('add', rv.get_data(as_text=True).lower())


class PostModelTestCase(SetupTearDownMixin, unittest.TestCase):

    def setUp(self):
        app.app.config['TESTING'] = True
        app.app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.app.test_client()

    def test_empty_database(self):
        rv = self.app.get('/')
        self.assertIn("there are no posts made yet. log in to make one!", rv.get_data(as_text=True).lower())

    def test_post_on_homepage(self):
        rv = self.app.post('/login', data=USER_DATA)
        rv = self.app.get('/')
        self.assertNotIn("there are no posts made yet. log in to make one!", rv.get_data(as_text=True).lower())
        self.assertIn('test', rv.get_data(as_text=True).lower())


    def test_post_create(self):
        post_data = {
            'title': 'Test',
            'date': '2015-09-09',
            'time_spent': '50 minutes',
            'what_i_learned': 'A lot of stuff',
            'resources_to_remember': 'Revise, alot'
        }

        rv = self.app.post('/login', data=USER_DATA)
        rv = self.app.post('/new', data=post_data)
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, 'http://localhost/')
        self.assertEqual(Post.select().count(), 1)

    def test_zedit_post(self):
        post_data1 = {
            'title': 'tesfddfasadfdafsdafsste',
            'date': '2015-09-09',
            'time_spent': '50 minutes',
            'what_i_learned': 'A lot of stuff',
            'resources_to_remember': 'Revise, alot'
        }

        rv = self.app.post('/login', data=USER_DATA)
        rv = self.app.post('/detail/1/edit', data=post_data1)
        rv = self.app.get('/')
        self.assertIn(post_data1['title'], rv.get_data(as_text=True).lower())


    def test_delete_post(self):
        post_data = {
            'title': 'teste',
            'date': '2015-09-09',
            'time_spent': '50 minutes',
            'what_i_learned': 'A lot of stuff',
            'resources_to_remember': 'Revise, alot'
        }

        rv = self.app.post('/login', data=USER_DATA)
        rv = self.app.post('/new', data=post_data)
        rv = self.app.get('detail/1/delete')
        rv = self.app.get('/')
        self.assertIn("there are no posts made yet. log in to make one!", rv.get_data(as_text=True).lower())
        self.assertEqual(Post.select().count(), 0)



#datetime in form posting should be date of today prefilled.


if __name__ == '__main__':
    unittest.main()



import unittest
import os
from flaskblog import app, db
from flaskblog.models import User, Post, Sportsmen
from datetime import datetime
# import flaskapi
import requests



class TestsDatabase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site14.db'

    def tearDown(self):
        db.session.close()

    def test_existence_of_admin(self):
        dfdf = User.query.get(1)
        self.assertEqual(dfdf.username, "admin")
        self.assertEqual(dfdf.email, "admin@example.com")

    def test_existence_of_users(self):
        dfdf = User.query.get(2)
        self.assertNotEqual(dfdf.username, "admin")
        self.assertNotEqual(dfdf.email, "admin@example.com")

    def test_avatar(self):
        dfdf = User.query.filter_by(username="admin").first()
        expected = 'https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?d=identicon&s=36'
        self.assertEqual(dfdf.avatar(36), expected)


    def test_follow(self):
        dfdf = User.query.filter_by(username="admin").first()
        dfdf2 = Sportsmen.query.filter_by(name="имя").first()
        fff = Sportsmen.query.filter_by(name="susan").first()

        dfdf.follow(fff)
        db.session.commit()

        self.assertTrue(dfdf.is_following(fff))
        self.assertEqual(dfdf.followed.count(), 3)
        self.assertEqual(dfdf.followed.filter_by(name="susan").first().name, 'susan')
        self.assertEqual(fff.followers.count(), 1)
        self.assertEqual(fff.followers.first().username, 'admin')


    def test_unfollow(self):
        dfdf = User.query.filter_by(username="admin").first()
        dfdf2 = Sportsmen.query.filter_by(name="имя").first()
        fff = Sportsmen.query.filter_by(name="susan").first()

        self.assertTrue(dfdf.is_following(fff))
        dfdf.unfollow(fff)
        db.session.commit()

        self.assertFalse(dfdf.is_following(fff))
        self.assertEqual(dfdf.followed.count(), 2)
        self.assertEqual(fff.followers.count(), 0)


    def test_following(self):
        dfdf = User.query.filter_by(username="admin").first()
        dfdf2 = Sportsmen.query.filter_by(name="имя").first()
        fff = Sportsmen.query.filter_by(name="susan").first()

        self.assertIsNotNone(dfdf.followed.all())
        self.assertIsNotNone(dfdf2.followers.all())


class PageLoadTest(unittest.TestCase):
    def test_home(self):
        response = requests.get('http://127.0.0.1:5000/home')
        self.assertEqual(response.status_code, 200)

    def test_account(self):
        response = requests.get('http://127.0.0.1:5000/account', allow_redirects=False)
        self.assertEqual(response.status_code, 401)

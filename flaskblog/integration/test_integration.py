import unittest
from flaskblog import app, db
from flaskblog.models import User, Sportsmen
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
        person = User.query.get(1)
        self.assertEqual(person.username, "admin")
        self.assertEqual(person.email, "admin@example.com")

    def test_existence_of_users(self):
        person = User.query.get(2)
        self.assertNotEqual(person.username, "admin")
        self.assertNotEqual(person.email, "admin@example.com")

    def test_avatar(self):
        person = User.query.filter_by(username="admin").first()
        expected = 'https://www.gravatar.com/avatar/e64c7d89f26bd1972efa854d13d7dd61?d=identicon&s=36'
        self.assertEqual(person.avatar(36), expected)

    def test_follow(self):
        person = User.query.filter_by(username="admin").first()
        # person2 = Sportsmen.query.filter_by(name="имя").first()
        person3 = Sportsmen.query.filter_by(name="susan").first()

        person.follow(person3)
        db.session.commit()

        self.assertTrue(person.is_following(person3))
        self.assertEqual(person.followed.count(), 3)
        self.assertEqual(person.followed.filter_by(name="susan").first().name, 'susan')
        self.assertEqual(person3.followers.count(), 1)
        self.assertEqual(person3.followers.first().username, 'admin')

    def test_unfollow(self):
        person = User.query.filter_by(username="admin").first()
        # person2 = Sportsmen.query.filter_by(name="имя").first()
        person3 = Sportsmen.query.filter_by(name="susan").first()

        self.assertTrue(person.is_following(person3))
        person.unfollow(person3)
        db.session.commit()

        self.assertFalse(person.is_following(person3))
        self.assertEqual(person.followed.count(), 2)
        self.assertEqual(person3.followers.count(), 0)

    def test_following(self):
        person = User.query.filter_by(username="admin").first()
        person2 = Sportsmen.query.filter_by(name="имя").first()

        self.assertIsNotNone(person.followed.all())
        self.assertIsNotNone(person2.followers.all())


class PageLoadTest(unittest.TestCase):
    def test_home(self):
        response1 = requests.get('http://127.0.0.1:5000/home')
        # print(response1.status_code, "test_home")
        self.assertEqual(response1.status_code, 200)

    def test_account(self):
        response2 = requests.get('http://127.0.0.1:5000/account', allow_redirects=False)
        # print(response2.status_code, "test_account")
        self.assertEqual(response2.status_code, 302)

    def test_adminpage(self):
        response3 = requests.get('http://127.0.0.1:5000/admin', allow_redirects=False)
        self.assertEqual(response3.status_code, 404)
        # print(response3.status_code, "test_adminpage")

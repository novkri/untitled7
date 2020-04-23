import os
import unittest

from flaskblog import app, db
from flaskblog.models import User
from coverage import coverage
cov = coverage(branch=True, omit=['flask/*', 'tests.py'])
cov.start()

from flaskblog import app, db
import unittest
from flask_login import current_user
from unittest import TestCase
from flaskblog.models import User
from flask_security.utils import login_user
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, login_manager
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post, Sportsmen, Event, Comment
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from flask import Flask
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime, timedelta



class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site14.db'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(username = 'john', email = 'john@example.com', password='12345')
        avatar = u.avatar(36)
        print(avatar, type(avatar))
        expected = 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=36'
        assert avatar[0:len(expected)] == expected

#
    # def test_correct_login(self):
    #     # Заглушка
    #     u = User(username='john', email='john@example.com', password='12345')
    #     db.session.add(u)
    #     db.session.commit()
    #     # тест
    #     with app.test_request_context('/login'):
    #         form = LoginForm()
    #         #form.validate_on_submit()
    #         # input:
    #         UFO_user = User(username='john', email='john@example.com', password='12345')
    #        # UFO_user = u.query.filter_by(email=f"john@example.com").first()
    #         print(UFO_user)
    #         if UFO_user.password == u.password:
    #             login_user(u, remember=form.remember.data)
    #             #self.assertEqual(UFO_user and u.password, '12345')
    #             print("Пароли совпадают")
    #         if current_user.is_authenticated:
    #             print("current user is authenticated")
    #     #self.assertIsInstance(form, LoginForm)
    #     print(u.is_authenticated)
    #     self.assertTrue(u.is_authenticated)
    #
    # def test_incorrect_login(self):
    #     # Заглушка
    #     u = User(username='john', email='john@example.com', password='12345')
    #     db.session.add(u)
    #     db.session.commit()
    #     # тест
    #     with app.test_request_context('/login'):
    #         form = LoginForm()
    #        # form.validate_on_submit()
    #         UFO_user = u.query.filter_by(email=f"john2@example.com").first()
    #         print(UFO_user)
    #     self.assertIsNone(UFO_user)
    #
    #
    # def test_incorrect_password(self):
    #     # Заглушка
    #     u = User(username='john', email='john@example.com', password='12345')
    #     db.session.add(u)
    #     db.session.commit()
    #     # тест
    #     with app.test_request_context('/login'):
    #         form = LoginForm()
    #        # form.validate_on_submit()
    #         UFO_user = User(username='john', email='john@example.com', password='123456')
    #         self.assertNotEqual(UFO_user.password, u.password)


# Тест на подписки
    def test_following(self):
        u1 = User(username='john', email='john@example.com', password='12345')
        s1 = Sportsmen(name='susan', biography='dummy data')
        db.session.add(u1)
        db.session.add(s1)
        db.session.commit()

        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(s1.followers.all(), [])

        u1.follow(s1) # подписка
        db.session.commit()

        self.assertTrue(u1.is_following(s1))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().name, 'susan')
        self.assertEqual(s1.followers.count(), 1)
        self.assertEqual(s1.followers.first().username, 'john')

        u1.unfollow(s1)

        db.session.commit()

        self.assertFalse(u1.is_following(s1))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(s1.followers.count(), 0)



if __name__ == '__main__':
    try:
        unittest.main()
    except:
        pass
    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join(basedir, "tmp/coverage/index.html"))
    cov.html_report(directory='tmp/coverage')
    cov.erase()


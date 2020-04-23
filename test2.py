import os
import unittest

from flaskblog import app, db
from flaskblog.models import User, Post, Sportsmen
from datetime import datetime

class TestCase(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(username='john', email='john@example.com', password='12345')
        avatar = u.avatar(36)
        expected = 'https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=36'
        self.assertEqual(avatar, expected)

    def test_following(self):
        u1 = User(username='john', email='john@example.com', password='12345')
        s1 = Sportsmen(name='susan', biography='dummy data')
        db.session.add(u1)
        db.session.add(s1)
        db.session.commit()

        self.assertFalse(u1.is_following(s1))
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(s1.followers.all(), [])

        u1.follow(s1)
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

    def test_posts(self):
        u = User(username='john', email='john@example.com', password='12345')
        p = Post(title='testpost', content='test post body', author=u, date_posted=datetime.utcnow())
        db.session.add(u)
        db.session.add(p)
        db.session.commit()
        self.assertIsNotNone(Post.query.get(1))

        db.session.delete(p)
        db.session.commit()
        self.assertIsNone(Post.query.get(1))


if __name__ == '__main__':
    unittest.main()

# работа с данными
from datetime import datetime

import login

from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('sportsmen.id'))
)


subs = db.Table('subs',
                db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                db.Column('sportsmen_id', db.Integer, db.ForeignKey('sportsmen.id'))
                )




class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.Column(db.Integer, default=0)
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


sport_event = db.Table('sport_event',
                db.Column('sportsmen_id', db.Integer, db.ForeignKey('sportsmen.id')),
                db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
                )



class Sportsmen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    biography = db.Column(db.Text, nullable=False)
    taking_parts = db.relationship('Event', secondary=sport_event, backref=db.backref('sport_event', lazy='dynamic'))

    def __repr__(self):
        return f"Sportsmen('{self.name}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    desc = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Event('{self.name}', '{self.date}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    message = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    post = db.relationship('Post', backref=db.backref('post'), lazy=True)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Comment('{self.username}')"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    subscriptions = db.relationship('Sportsmen', secondary=subs, backref=db.backref('subscribers', lazy='dynamic'))
    followed = db.relationship('Sportsmen', secondary=followers,
        # primaryjoin='followers.c.follower_id == User.id',
        # secondaryjoin='followers.c.followed_id == Sportsmen.id',
        backref=db.backref('followers', lazy='dynamic') )
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def follow(self, sportsmen):
        if not self.is_following(sportsmen):
            self.followed.append(sportsmen)

    def unfollow(self, sportsmen):
        if self.is_following(sportsmen):
            self.followed.remove(sportsmen)

    def is_following(self, sportsmen):
        return self.followed.filter(
            followers.c.followed_id == sportsmen.id).count() > 0

    # def followed_posts(self):
    #     followed = Sportsmen.query.join(
    #         followers, (followers.c.followed_id == Sportsmen.id)).filter(
    #         followers.c.follower_id == self.id)
    #     #own = Post.query.filter_by(user_id=self.id)
    #     return followed
    #         #.union(own)
    #         #.order_by(Sportsmen.id.desc())

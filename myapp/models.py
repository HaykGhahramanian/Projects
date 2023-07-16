from flask_login import UserMixin
from app import db
from datetime import datetime


class Users_Tweets(db.Model):
    __tablename__ = 'users_tweets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))

    user = db.relationship('User', backref='users_tweets')
    tweet = db.relationship('Tweets', backref='users_tweets')


class Tweets(db.Model):
    __tablename__ = 'tweets'

    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    photo = db.Column(db.String(255))

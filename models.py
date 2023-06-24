from flask_login import UserMixin
from app import db


class Users_Tweets(db.Model):
    __tablename__ = 'userstweets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweets.id'))

    user = db.relationship('User', backref=db.backref('users_tweets', lazy='dynamic'))
    tweet = db.relationship('Tweets', backref=db.backref('users_tweets', lazy='dynamic'))


class Tweets(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True)
    letter = db.Column(db.String(255))
    date_created = db.Column(db.DateTime)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(15))
    email = db.Column(db.String(30))
    photo = db.Column(db.String(350))


"""from app import app, db

app_ctx = app.app_context()
app_ctx.push()

db.create_all()

app_ctx.pop()"""

# export FLASK_APP=models.py
# flask db init
# flask db migrate -m "Create Users_Tweets table"
# flask db upgrade


"""from app import app, db

app_ctx = app.app_context()
app_ctx.push()

db.drop_all()

app_ctx.pop()"""

from os.path import dirname
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

home = dirname(dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{HOME}/database/tweeter.db'.format(HOME=home)
db = SQLAlchemy(app)

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(254), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

class Event(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(15))
    pub_date = db.Column(db.DateTime, nullable=False)
    consumed = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('events', lazy='dynamic'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=False)
    tweet = db.relationship('Tweet', backref=db.backref('events', lazy='dynamic'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    playlist = db.relationship('Playlist', backref=db.backref('events', lazy='dynamic'))
    shuffle = db.Column(db.Boolean)

    def __init__(self, user, tweet, pub_date, recipient=None, consumed=False, playlist=None, shuffle=False):
        self.user = user
        self.tweet = tweet
        self.pub_date = pub_date
        self.recipient = recipient
        self.consumed = consumed
        self.playlist = playlist
        self.shuffle = shuffle

class Tweet(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy='dynamic'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    playlist = db.relationship('Playlist', backref=db.backref('tweets', lazy='dynamic'))
    
    def __init__(self, content, user, playlist=None):
        self.content = content
        self.user = user
        self.playlist = None

class Playlist(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('playlists', lazy='dynamic'))
    
    def __init__(self, name, user):
        self.name = name
        self.user = user
        
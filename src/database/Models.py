from os.path import dirname
import tweepy
from datetime import datetime, timedelta
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from Scheduled import Scheduled

home = dirname(dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////{HOME}/data/tweeter.db'.format(HOME=home)
db = SQLAlchemy(app)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(254), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def tweet(self, event):
        #=======================================================================
        # Dispatcher to the appropriate API call
        # based on the event type.
        #=======================================================================
        if event.messageType == Event.TWEET:
            return self._tweet(event)
        elif event.messageType == Event.DIRECT_MESSAGE:
            return self._directMessage(event)
        
    def _tweet(self, event):
        raise NotImplemented()
    
    def _directMessage(self, event):
        raise NotImplemented()

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

class Series(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('series', lazy='dynamic'))
    
    def __init__(self, user):
        self.user = user

class Event(db.Model):

    TWEET = 'tweet'
    DIRECT_MESSAGE = 'direct_message'
    DELTAS = {
              'DAILY': timedelta(days=1),
              'WEEKLY': timedelta(weeks=1),
              'MONTHLY':  timedelta(months=1)
              }

    id = db.Column(db.Integer, primary_key=True)
    recipient = db.Column(db.String(15))
    pub_date = db.Column(db.DateTime, nullable=False)
    messageType = db.Column(db.String(14))
    consumed = db.Column(db.Boolean)
    repeated = db.Column(db.Boolean)
    delta = db.Column(db.Integer)
    repetitions = db.Column(db.Integer)
    maxRepetitions = db.Column(db.Integer)
    endDate = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('events', lazy='dynamic'))
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'), nullable=False)
    tweet = db.relationship('Tweet', backref=db.backref('events', lazy='dynamic'))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    playlist = db.relationship('Playlist', backref=db.backref('events', lazy='dynamic'))
    series_id = db.Column(db.Integer, db.ForeignKey('series.id'))
    series = db.relationship('Playlist', backref=db.backref('events', lazy='dynamic'))
    shuffle = db.Column(db.Boolean)

    def __init__(self, user, tweet, pub_date, repeated=False, delta=None, messageType=Event.TWEET,
                 repetitions=0, maxRepetitions=0, endDate=None, recipient=None,
                 consumed=False, playlist=None, shuffle=False, series=None
                 ):
        self.user = user
        self.tweet = tweet
        self.pub_date = pub_date
        self.messageType = messageType
        self.repeated = repeated
        self.delta = delta
        self.repetitions = repetitions
        self.maxRepetitions = maxRepetitions
        self.endDate = endDate
        self.recipient = recipient
        self.consumed = consumed
        self.playlist = playlist
        self.shuffle = shuffle
        self.series = series
    
    @Scheduled
    def enqueue(self):
        self.user.tweet(self)
        self.consumed = True
        if self.shouldReplicate:
            self.replicate()

    def replicate(self):
        event = Event(
            user=self.user,
            tweet=self.tweet,
            pub_date=self.pub_date + self.delta,
            repeated = self.repeated,
            delta = self.delta,
            messageType = self.messageType,
            repetitions=self.repetitions + 1,
            maxRepetitions=self.maxRepetitions,
            endDate=self.endDate,
            recipient=self.recipient,
            playlist=self.playlist,
            shuffle=self.shuffle,
            series=self.series
            )
        db.session.add(event)
        db.session.commit()

    @property
    def shouldReplicate(self):
        if self.maxRepetitions:
            #===================================================================
            # User defined a maximum number of repetitions for this event.
            #===================================================================
            return self.repetitions < self.maxRepetitions
        elif self.endDate:
            #===================================================================
            # User defined an ending date for this event.
            #===================================================================
            return self.pub_date + self.delta <= self.endDate
        else:
            #===================================================================
            # If true, user defined this event to repeat forever.
            # Else, this was a one time event.
            #===================================================================
            return self.repeated
    
    @property
    def timeUntilEvent(self):
        return (self.pub_date - datetime.now(self.pub_date.tzinfo)).total_seconds()
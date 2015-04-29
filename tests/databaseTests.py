from os.path import dirname
import sys
import unittest
from datetime import datetime
sys.path.append("{HOME}/src/database/".format(HOME=dirname(dirname(__file__))))
from Models import *

class TestUser(unittest.TestCase):
    
    def setUp(self):
        db.drop_all()
        db.create_all()
        user = User(name='J.R. Bob Dobbs', email='dobbs@subgenius.org')
        db.session.add(user)
        db.session.commit()
    
    def testGetUserByName(self):
        user = User.query.filter_by(name='J.R. Bob Dobbs').first()
        assert isinstance(user, User)
        assert user.name == 'J.R. Bob Dobbs'
        assert user.id == 1
        assert user.email == 'dobbs@subgenius.org'

class TestTweets(unittest.TestCase):
    
    def setUp(self):
        db.drop_all()
        db.create_all()
        user = User(name='J.R. Bob Dobbs', email='dobbs@subgenius.org')
        tweet = Tweet(
            content = 'Hello from the testing world.',
            user = user
        )
        db.session.add(user)
        db.session.add(tweet)
        db.session.commit()
    
    def testRelationship(self):
        user = User.query.filter_by(name='J.R. Bob Dobbs').first()
        tweet = Tweet.query.all()[0]
        assert user.tweets[0] is tweet
        assert tweet.user is user


unittest.main()
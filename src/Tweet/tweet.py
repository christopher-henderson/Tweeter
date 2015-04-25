from quote import Quote
from ConfigService import Config
from random import randrange
import tweepy

class Tweet(object):
    
    TWEETS = [Quote(Config.recipient(), quote) for quote in Config.quotes()]
    AGED_TWEETS = []
    AUTH = tweepy.OAuthHandler(Config.consumer_key(), Config.consumer_secret())
    AUTH.set_access_token(Config.access_token(), Config.access_token_secret())
    INSPIRATION = tweepy.API(AUTH)

    def __init__(self):
        self.tweet = self._generateTweet()
        self()

    def __unicode__(self):
        return unicode(self.tweet)

    def __str__(self):
        return str(self.tweet)
    
    def __repr__(self):
        return self.tweet.__repr__()

    def __call__(self):
        try:
            self.INSPIRATION.update_status(status=unicode(self))
        except:
            #===================================================================
            # Probably a network error of some kind. There are a number
            # of ways I can handle this. For example, I can try to build a
            # queue for messages that fail.
            # 
            # But what I'm actually going to do is ignore it and try again
            # next time.
            #===================================================================
            pass

    def _generateTweet(self):
        if len(self.TWEETS) is 0:
            self.TWEETS = self.AGED_TWEETS
            self.AGED_TWEETS = []
        tweet = self.TWEETS.pop(randrange(len(self.TWEETS)))
        self.AGED_TWEETS.append(tweet)
        return tweet
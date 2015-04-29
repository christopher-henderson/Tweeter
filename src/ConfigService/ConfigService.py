from __future__ import absolute_import
from functools import wraps
from yaml import load, dump
from os.path import dirname
from pwd import getpwnam

def LazyLoad(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        if not self.config:
            self.loadConfig()
        return function(self, *args, **kwargs)
    return wrapper

class ConfigService(object):

    def __init__(self):
        self.config = None
        home = dirname(dirname(dirname(__file__)))
        self.configFile = '{HOME}/etc/inspiration.yaml'.format(HOME=home)
        self.tweeted = '{HOME}/etc/tweeted.yaml'.format(HOME=home)

    def __iter__(self):
        for section in self.config:
            yield self.config[section]

    def loadConfig(self):
        with open(self.configFile) as conf:
            self.config = load(conf)
    
    def reload(self):
        with open(self.tweeted, 'r') as aged:
            tweeted = load(aged)
        with open(self.tweeted, 'w') as aged:
            dump([], aged)
        self.config['quotes'] = tweeted
        self.save()

    def save(self):
        with open(self.configFile, 'w') as conf:
            dump(self.config, conf)

    def age(self, message):
        with open(self.tweeted, 'r') as aged:
            tweeted = load(aged)
        tweeted.append(message)
        with open(self.tweeted, 'w') as aged:
            dump(tweeted, aged)
        self.remove(message)

    def remove(self, message):
        index = self.config['quotes'].index(message)
        self.config['quotes'].pop(index)
        self.save()

    @LazyLoad
    def recipient(self):
        return self.config.get('recipient')
    
    @LazyLoad
    def quotes(self):
        return self.config.get('quotes')
    
    @LazyLoad
    def access_token(self):
        return self.config.get('access_token')
    
    @LazyLoad
    def access_token_secret(self):
        return self.config.get('access_token_secret')

    @LazyLoad
    def consumer_key(self):
        return self.config.get('consumer_key')

    @LazyLoad
    def consumer_secret(self):
        return self.config.get('consumer_secret')
    
    @LazyLoad
    def getUID(self):
        return getpwnam(self.config.get('USER')).pw_uid

    @LazyLoad
    def getGID(self):
        return getpwnam(self.config.get('USER')).pw_gid

    @LazyLoad
    def getPIDFile(self):
        return '/home/{USER}/{PID}'.format(USER=self.config.get('USER'), PID=self.config.get('PIDFILE'))

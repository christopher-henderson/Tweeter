from __future__ import absolute_import
from functools import wraps
from yaml import load
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

    def __iter__(self):
        for section in self.config:
            yield self.config[section]

    def loadConfig(self):
        home = dirname(dirname(dirname(__file__)))
        configFile = '{HOME}/etc/inspiration.yaml'.format(HOME=home)
        with open(configFile) as conf:
            self.config = load(conf)
    
    def reload(self):
        self.loadConfig()
    
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

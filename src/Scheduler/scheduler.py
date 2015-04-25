from Tweet import Tweet
import schedule
from functools import wraps
from threading import Thread
from time import sleep

def Threaded(function):
    '''
    Every call of the decorated function will spawn a
    daemonized thread. Returns a threading.Thread object.
    '''
    @wraps(function)
    def wrapper(*args, **kwargs):
        thread = Thread(target=function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper

class Scheduler(object):

    @staticmethod
    @Threaded
    def start():
        while True:
            schedule.run_pending()
            sleep(30)

    @staticmethod
    def add(day, time):
        schedule.every().__getattribute__(day).at(time).do(Tweet)
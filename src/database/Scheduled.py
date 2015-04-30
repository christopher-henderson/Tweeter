from functools import wraps
from threading import Timer

def Scheduled(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        thread = Timer(self.timeUntilEvent, function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper
from functools import wraps
from threading import Timer

#===============================================================================
# There are so many design decisions that go into this one module.
# 
# First, context:
# 
#     1). This project is essentially a direct competitor to a
#         service already sold by Twitter.
#     2). Therefore this project is largely academic as I have
#         no sincere interest in attracting enterprise use.
#     3). Therefore the average load on this application will
#         likely be minimal.
# 
# What does this effect?
# 
#     1). Database to use.
#     2). Threading scheme.
#     3). Scheduling scheme.
# 
# Database:
#     
#     SQLite is dead easy and fast for small applications. There
#     will not be network access to the database and there will not
#     be multiple processes accessing the database. The nagging
#     question is, "What if...?". Well, what if nothing. If I decide
#     to switch to a client/server DB then that should not be too
#     aggregious. Still, keep it in mind.
# 
# Threading Scheme:
# 
#     It terms of scaling this to a large system, having a worker pool
#     via multiprocessing.Pool would be dead sexy and consistent with
#     the strategy of many web applications. This, however, increases
#     complexity and creates multiple readers/writers to the database - a
#     no no for SQLite. Besides, this application is hardly CPU bound in
#     any way. The bottleneck is in network IO on a free tier AWS server
#     with one NIC. Essentially, without customers to pay for a more
#     appropriate server, concurrency instead of parallelism seems to be
#     the way to go.
# 
# Scheduling Scheme:
# 
#     There are any number of ways to schedule these events. The most
#     desirable is a simple timer based interrupt. Unfortunately I do
#     not believe this is something that is possible in pure Python.
#     The simplest solution is put a sleep in the thread, however this
#     creates a thread that is unresponsive (what if the user cancels
#     events? The thread for a pending Tweet MUST be halted!). Modules
#     such as 'schedule' (https://pypi.python.org/pypi/schedule) work by
#     registering events and then spin-polling for events to fire - rather
#     unsatisfactory. There do exist large scheduling frameworks
#     (such as Celery), but these are too hefty and complicated in the context
#     of this project.
#     
#     So what I'm going to do is use threading.Timer. This is a compromise
#     between an unresponsive sleep and spin-polling. Timer's implementation
#     is as follows:
# 
#     https://github.com/python-git/python/blob/master/Lib/threading.py#L228
#     
#     So it is a mix of sleeping and polling, but done in a nice package for me.
#===============================================================================

def Scheduled(function):
    @wraps(function)
    def wrapper(self, *args, **kwargs):
        thread = Timer(self.timeUntilEvent, function, args=args, kwargs=kwargs)
        thread.daemon = True
        thread.start()
        return thread
    return wrapper
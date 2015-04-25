from functools import wraps
from ConfigService import Config
import daemon
from lockfile import FileLock

def Daemonize(function):
    '''
    Decorates a function that will be ran as a well behaved Unix daemon.
    '''
    @wraps(function)
    def wrapper(*args, **kwargs):
        #=======================================================================
        # This is interesting.
        # 
        # What is happening here is that the python-daemon module is asking itself
        # if we are daemonizing something from a "superserver". How the author chose
        # to determine this was to see if main's stdin is actually a socket. However, the
        # multiprocess.Process that is calling this code has already taken it upon
        # itself to close the stdin file, resulting in an I/O error.
        # 
        # Really, the answer to this question is "no". So here we are, just saying "no".
        #=======================================================================
        if hasattr(daemon.daemon, 'is_process_started_by_superserver'):
            daemon.daemon.is_process_started_by_superserver = lambda: False
        #===================================================================
        #===================================================================
        context = daemon.DaemonContext(
            detach_process=True,
            working_directory = '/',
            uid = Config.getUID(),
            gid = Config.getGID(),
            pidfile=FileLock(Config.getPIDFile())
            )
        with context:
            try:
                function(*args, **kwargs)
            except Exception as e:
                print (e)
    return wrapper
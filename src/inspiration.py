from Scheduler import Scheduler
from Tools import Daemonize
from time import sleep

@Daemonize
def main():
    Scheduler.add('monday', '6:00')
    Scheduler.add('wednesday', '6:00')
    Scheduler.add('friday', '6:00')
    Scheduler.start()
    oneYear = 60*60*24*365
    while True:
        sleep(oneYear)

if __name__ == '__main__':
    print ("Starting inspiration server...")
    try:
        main()
    except Exception as error:
        print ("Start [\033[91mFAIL\033[0m]")
        print (error)
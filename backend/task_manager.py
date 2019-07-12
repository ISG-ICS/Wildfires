import threading
import time
import argparse
from data_preparation.crawler.windcrawler import WindCrawler


class task_manager(object):
    """ThM (ThreadManager)
    Handles very simple thread operations:
        Creating single-shot threads -> ThM.run(...)
        Creating 'looping per interval' threads -> ThM.run(...) with loop set to True
        Stopping looping threads based on name -> ThM.stop_loop(...)
        Joining all threads into the calling thread ThM.joinall()
        Removing stopped threads from 'running_threads' - > ThM.free_dead()


    The class has been designed for very simple operations, mainly
    for programs that need "workers" that mindlessly loop over a function.

    NOTE: Locks,Events,Semaphores etc. have not been taken into consideration
    and may cause unexpected behaviour if used!
     """
    running_threads = []

    @classmethod
    def run(cls, targetfunc, thname, loop, interval, arglist=[]):
        """Statrs a new thread and appends it to the running_threads list
        along with the specified values.
        Loop and interval needs to be specified even if you dont
        want it to loop over. This is to avoid lot of keyword arguments
        and possible confusion.
        Example of starting a looping thread:
            ThM.run(function,"MyThreadName",True,0.5,[1,2,"StringArguemnt"])

        To stop it, use:
            ThM.stop_loop("MyThreadName")
        Note, a stopped thread cannot be started again!

        Example of a single-shot thread:
            ThM.run(function,"ThreadName",False,0.5,[1,2,"StringArgument"])
            """

        th = threading.Thread(target=cls._thread_runner_, args=(targetfunc, thname, interval, arglist))
        th.setDaemon(True)
        cls.running_threads.append([th, thname, loop])
        th.start()

    @classmethod
    def free_dead(cls):
        """Removes all threads that return FALSE on isAlive() from the running_threads list """
        for th in cls.running_threads[:]:
            if th[0].isAlive() == False:
                cls.running_threads.remove(th)

    @classmethod
    def stop_loop(cls, threadname):
        """Stops a looping function that was started with ThM.run(...)"""
        for i, thlis in enumerate(cls.running_threads):
            if thlis[1] == threadname:
                cls.running_threads[i][2] = False
                break

    @classmethod
    def joinall(cls):
        """Joins all the threads together into the calling thread."""
        for th in cls.running_threads[:]:
            while th[0].isAlive():
                time.sleep(0.1)
            th[0].join()
        #   print "Thread:",th[1],"joined","isalive:",th[0].isAlive() --- Debug stuff

    @classmethod
    def get_all_params(cls):
        """Returns parameters from the running_threads list for external manipulation"""
        for thli in cls.running_threads:
            yield (thli[0], thli[1], thli[2])

    # This method is only intended for threads started with ThM !
    @classmethod
    def _thread_runner_(cls, targetfunc, thname, interval, arglist):
        """Internal function handling the running and looping of the threads
        Note: threading.Event() has not been taken into consideration and neither the
        other thread managing objects (semaphores, locks, etc.)"""
        indx = 0
        for thread in cls.running_threads[:]:
            if thname == thread[1]:
                break
            indx += 1
        targetfunc(*arglist)
        while cls.running_threads[indx][2] == True:
            if interval != 0:
                time.sleep(interval)
            targetfunc(*arglist)






if __name__ == "__main__":

    wind_crawler = WindCrawler()

    task_manager = task_manager()

    #Add crawler to the crawlers menu, all crawler instance
    crawlers = {
        1:["windcrawler-",wind_crawler,0]
    }
    crawler_loop = False
    crawler_interval = 0
    while True:
        print ("#"*80)
        print ("#"+ "".center(78," ")+"#")
        print ("#"+ "".center(78," ")+"#")
        print ("#"+ "Welcome to wildfire Crawler Manager".center(78," ")+"#")
        print ("#"+ "Update: Add wind crawler".center(78," ")+"#")
        print ("#"+ "Version 0.1".center(78," ")+"#")
        print ("#"+ "Credit to Unicorn".center(78," ")+"#")
        print ("#"+ "".center(78," ")+"#")
        print ("#"+ "".center(78," ")+"#")
        print ("#"*80)

        #Clear finished thread
        task_manager.free_dead()
        print("You have following crawler running in loop")
        for i,thread in enumerate(task_manager.running_threads):
            if (thread[2] == True):
                print( "[%d]: %s"%(i, thread[1]))
        print("Enter the crawler Number to stop the crawler")
        try:
            stop_crawler_prompt = input("if you don't want to break the loop press any key to continue\n")
            stop_crawler_prompt = int(stop_crawler_prompt)
            task_manager.stop_loop(task_manager.running_threads[stop_crawler_prompt][1])
        except:
            print(" Skipped, no crawler been terminated ");
        crawler_prompt = input("Which Crawler would you like to run [1].Wind [2].Temprature [3].Moisture [q] quit\n")
        crawler_prompt = crawler_prompt.strip()
        crawler_prompt = crawler_prompt.lower()
        if crawler_prompt == 'q':
            break;
        else:
            crawler_prompt = int(crawler_prompt)

        loop_prompt = input("Would you like to run crawler in a loop? yes/no ([y]/[n]) or [q] for quit\n")
        loop_prompt = loop_prompt.strip()
        loop_prompt = loop_prompt.lower()

        if loop_prompt == 'q':
            break
        elif loop_prompt == 'y':
            crawler_loop = True

        interval_prompt = input("Interval between each run enter a NUMBER of seconds\n")
        try:
            interval_prompt = int(interval_prompt)

            task_manager.run(targetfunc=crawlers[crawler_prompt][1].start,thname=crawlers[crawler_prompt][0]+str(crawlers[crawler_prompt][2]),loop=crawler_loop,interval=interval_prompt)
            # Increment id of this type of crawler
            crawlers[crawler_prompt][2]+=1
            print(crawlers[crawler_prompt][2])
            print("Your crawler is running!")
        except Exception as e:
            print("[Error] Your input is not all correct, the crawler has not started")

















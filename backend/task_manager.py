import threading
import time
import rootpath
rootpath.append()
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
    task_options = {}
    task_option_id = 1

    @classmethod
    def add_task_option(cls,task_name,task_func,task_number):
        '''
        :param task_name: name of this task option
        :param task_func: the runnable of this task
        :param task_number: id of this next task eg. let's say we had a wind_crawler-1 is running, to make our second wind crawler's name unique
        we increment this number, so next wind crawler task will be called wind_crawler-2
        :return: None
        '''
        cls.task_options.__setitem__(cls.task_option_id,[task_name,task_func,task_number])
        cls.task_option_id += 1

    @classmethod
    def delete_task_option(cls,task_option_id):
        '''
        :param task_option_id: id of task option you want to delete
        :return: None
        '''
        cls.task_options.pop(task_option_id)

    @classmethod
    def task_option_to_string(cls):
        '''

        :return: formated tasks in the current task option dictionary
        '''
        to_return = ""
        task_template = "[%d].%s%d "
        for option in cls.task_options:
            to_return += task_template%(option,cls.task_options[option][0],cls.task_options[option][2])

        return to_return

    @classmethod
    def run(cls, task_option_id, loop, interval, arglist=[]):
        '''

        :param task_option_id: task id for task in the task option list
        :param loop:  determine is this is a looped task
        :param interval: time between each execution of the looped task
        :param arglist: argument for the task
        :return: None
        '''

        targetfunc = cls.task_options[task_option_id][1]
        thname = cls.task_options[task_option_id][0]+str(cls.task_options[task_option_id][2])
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
    task_manager.add_task_option("windcrawler-",wind_crawler.start,0)
    task_loop = False

    while True:
        print ("#"*80)
        print ("#"+ "".center(78," ")+"#")
        print ("#"+ "".center(78," ")+"#")
        print ("#"+ "Welcome to wildfire Task Manager".center(78," ")+"#")
        print ("#"+ "Update: Bind task options to task_manager class".center(78," ")+"#")
        print ("#"+ "Version 0.2".center(78," ")+"#")
        print ("#"+ "Credit to Unicorn".center(78," ")+"#")
        print ("#"+ "".center(78," ")+"#")
        print ("#"+ "".center(78," ")+"#")
        print ("#"*80)

        #Clear finished thread
        task_manager.free_dead()
        print("You have following task running in loop")
        for i,thread in enumerate(task_manager.running_threads):
            if (thread[2] == True):
                print( "[%d]: %s"%(i, thread[1]))
        print("Enter the task Number to stop the task")
        try:
            stop_task_prompt = input("if you don't want to break the loop press any key to continue\n")
            stop_task_prompt = int(stop_task_prompt)
            task_manager.stop_loop(task_manager.running_threads[stop_task_prompt][1])
        except:
            print(" Skipped, no task been terminated ");
        task_prompt = input("Which task would you like to run "+task_manager.task_option_to_string()+" [q] quit\n")
        task_prompt = task_prompt.strip()
        task_prompt = task_prompt.lower()
        if task_prompt == 'q':
            break;
        else:
            task_prompt = int(task_prompt)

        loop_prompt = input("Would you like to run task in a loop? yes/no ([y]/[n]) or [q] for quit\n")
        loop_prompt = loop_prompt.strip()
        loop_prompt = loop_prompt.lower()

        if loop_prompt == 'q':
            break
        elif loop_prompt == 'y':
            task_loop = True

        interval_prompt = input("Interval between each run enter a NUMBER of seconds\n")
        try:
            interval_prompt = int(interval_prompt)
            task_manager.run(task_option_id=task_prompt,loop=task_loop,interval=interval_prompt)
            # Increment number of user specified task
            task_manager.task_options[task_prompt][2] += 1
            print("Your task is running!")
        except Exception as e:
            print(e)
            print("[Error] Your input is not all correct, the task has not started")

















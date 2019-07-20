import threading
import time

import rootpath

rootpath.append()
from backend.task.image_from_tweet import ImageFromTweet


class TaskManager:
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
    running_threads = list()
    task_options = dict()
    task_option_id = 1

    @classmethod
    def add_task_option(cls, runnable: type, task_params=None):
        """

        :param runnable: The Runnable class
        :param task_params: the runnable of this task

        :return: None
        """
        cls.task_options[cls.task_option_id] = (runnable, task_params)
        cls.task_option_id += 1

    @classmethod
    def delete_task_option(cls, task_option_id):
        """
        :param task_option_id: id of task option you want to delete
        :return: None
        """
        cls.task_options.pop(task_option_id)

    @classmethod
    def task_option_to_string(cls):
        """
        :return: formatted tasks in the current task option dictionary
        """
        return "\n".join(
            f"{option_id} - {runnable.__name__}" for option_id, (runnable, args) in cls.task_options.items())

    @classmethod
    def run(cls, task_option_id, loop, interval):
        """
        :param task_option_id: task id for task in the task option list
        :param loop:  determine is this is a looped task
        :param interval: time between each execution of the looped task
        :param args: argument for the task
        :return: None
        """
        print(cls.task_options)
        runnable, args = cls.task_options[task_option_id]
        print(runnable, args)
        if not args:
            args = (runnable(),)
        th_name = f"{runnable.__name__} + "
        th = threading.Thread(target=cls._thread_runner_, args=(runnable.run, args, th_name, interval))
        th.setDaemon(True)
        cls.running_threads.append([th, th_name, loop])
        th.start()

    @classmethod
    def free_dead(cls):
        """Removes all threads that return FALSE on isAlive() from the running_threads list """
        for th in cls.running_threads[:]:
            if not th[0].isAlive():
                cls.running_threads.remove(th)

    @classmethod
    def stop_loop(cls, thread_name):
        """Stops a looping function that was started with ThM.run(...)"""
        for i, thlis in enumerate(cls.running_threads):
            if thlis[1] == thread_name:
                cls.running_threads[i][2] = False
                break

    @classmethod
    def join_all(cls):
        """Joins all the threads together into the calling thread."""
        for th in cls.running_threads[:]:
            while th[0].isAlive():
                time.sleep(0.1)
            th[0].join()
        #   print "Thread:",th[1],"joined","isalive:",th[0].isAlive() --- Debug stuff

    @classmethod
    def get_all_params(cls):
        """Returns parameters from the running_threads list for external manipulation"""
        for th_list in cls.running_threads:
            yield (th_list[0], th_list[1], th_list[2])

    # This method is only intended for threads started with ThM !
    @classmethod
    def _thread_runner_(cls, target_func, args, th_name, interval):
        """Internal function handling the running and looping of the threads
        Note: threading.Event() has not been taken into consideration and neither the
        other thread managing objects (semaphores, locks, etc.)"""
        index_ = 0
        for thread_ in cls.running_threads[:]:
            if th_name == thread_[1]:
                break
            index_ += 1

        target_func(*args if args else tuple())
        while cls.running_threads[index_][2]:
            if interval != 0:
                time.sleep(interval)
            target_func(*args)

    @classmethod
    def main_loop(cls):
        cls.task_loop = False
        cls.load_task_options()
        while True:

            print(

                "################################################################################\n"
                "#                                                                              #\n"
                "#                                                                              #\n"
                "#                       Welcome to wildfire Task Manager                       #\n"
                "#               Update: Bind task options to task_manager class                #\n"
                "#                                 Version 0.2                                  #\n"
                "#                              Credit to Unicorn                               #\n"
                "#                                                                              #\n"
                "#                                                                              #\n"
                "################################################################################\n"
            )

            # Clear finished thread
            cls.free_dead()
            print("You have following task running in loop")
            for i, thread in enumerate(cls.running_threads):
                if thread[2]:
                    print("[%d]: %s" % (i, thread[1]))
            print("Enter the task Number to stop the task")
            try:
                stop_task_prompt = input("if you don't want to break the loop press any key to continue\n")
                stop_task_prompt = int(stop_task_prompt)
                cls.stop_loop(cls.running_threads[stop_task_prompt][1])
            except:
                print(" Skipped, no task been terminated ")
            task_prompt = input("Which task would you like to run " + cls.task_option_to_string() + " [q] quit\n")
            task_prompt = task_prompt.strip()
            task_prompt = task_prompt.lower()
            if task_prompt == 'q':
                break
            else:
                task_prompt = int(task_prompt)

            loop_prompt = input(
                "Would you like to run task in a loop? yes/no ([y]/[n]) or [q] for quit\n").strip().lower()

            if loop_prompt == 'q':
                break
            elif loop_prompt == 'y':
                cls.task_loop = True

            interval_prompt = input("Interval between each run enter a NUMBER of seconds\n")
            try:
                interval_prompt = int(interval_prompt)
                cls.run(task_option_id=task_prompt, loop=cls.task_loop, interval=interval_prompt)
                # Increment number of user specified task
                cls.task_options[task_prompt][2] += 1
                print("Your task is running!")
            except Exception as e:
                print(e)
                print("[Error] Your input is not all correct, the task has not started")

    @classmethod
    def load_task_options(cls):
        cls.task_options = {1: (ImageFromTweet, None)}


if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.main_loop()

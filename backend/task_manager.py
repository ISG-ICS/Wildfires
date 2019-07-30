import inspect
import json
import logging.config
import threading
import time
import traceback

import rootpath

rootpath.append()
from paths import LOG_CONFIG_PATH

# don't delete these imports because they're called implicitly
exec("from backend.task import *")


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
    exec("from backend.task.runnable import Runnable")
    running_threads = []
    task_options = {}
    # use 'Runnable' as parent class' name and get all the subclasses' names
    for i, sub_cls in enumerate(vars()['Runnable'].__subclasses__()):
        task_options[i + 1] = [sub_cls.__name__, sub_cls().run, 1]
    task_option_id = 1

    @staticmethod
    def initialize_logger():
        with open(LOG_CONFIG_PATH, 'r') as file:
            config = json.load(file)
            # use json file to config the logger
            logging.config.dictConfig(config)
            logger = logging.getLogger('TaskManager')
            info_format = '[%(asctime)s] [%(levelname)5s] [%(threadName)21s] [%(module)25s] [%(funcName)21s]: %(message)s'
            date_format = '%m/%d/%Y-%H:%M:%S'
            formatter = logging.Formatter(fmt=info_format, datefmt=date_format)
            handler_names = ['taskManager_info.log', 'taskManager_error.log']
            current_time = time.strftime('%m%d%Y_%H:%M:%S_', time.localtime(time.time()))
            for handler_name in handler_names:
                file_name = current_time + handler_name
                file_handler = logging.FileHandler(file_name, mode='a', encoding=None, delay=False)
                file_handler.setLevel(
                    logging.DEBUG if handler_name.split('.')[0].split('_')[-1] == 'info' else logging.ERROR)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        return logger

    @classmethod
    def add_task_option(cls, task_name, task_func, task_number):
        """
        :param task_name: name of this task option
        :param task_func: the runnable of this task
        :param task_number: id of this next task eg. let's say we had a wind_crawler-1 is running, to make our second
                            wind crawler's name unique
        we increment this number, so next wind crawler task will be called wind_crawler-2
        :return: None
        """
        cls.task_options.__setitem__(cls.task_option_id, [task_name, task_func, task_number])
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
        :return: formated tasks in the current task option dictionary
        """
        to_return = ""
        task_template = " [%d]: %s-%d \n"
        for option in cls.task_options:
            to_return += task_template % (option, cls.task_options[option][0], cls.task_options[option][2])

        return to_return

    @classmethod
    def run(cls, task_option_id, loop, interval, args=None):
        """
        :param task_option_id: task id for task in the task option list
        :param loop:  determine is this is a looped task
        :param interval: time between each execution of the looped task
        :param args: argument for the task
        :return: None
        """

        if args is None:
            args = []
        target_func = cls.task_options[task_option_id][1]
        th_name = cls.task_options[task_option_id][0] + str(cls.task_options[task_option_id][2])
        th = threading.Thread(target=cls._thread_runner_, args=(target_func, th_name, interval, args))
        logger.info('A new task will be running!')
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
                logger.info('TASK ' + cls.running_threads[i][1] + ' KILLED!')
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
    def _thread_runner_(cls, target_func, th_name, interval, args):
        """Internal function handling the running and looping of the threads
        Note: threading.Event() has not been taken into consideration and neither the
        other thread managing objects (semaphores, locks, etc.)"""
        index_ = 0
        for thread_ in cls.running_threads[:]:
            if th_name == thread_[1]:
                break
            index_ += 1
        logger.info('TASK ' + th_name + ' START!')
        target_func(*args)
        logger.info('TASK ' + th_name + ' END!')
        while cls.running_threads[index_][2]:
            if interval != 0:
                time.sleep(interval)
            target_func(*args)

    def pass_arguments(self, task_prompt):
        """get function run()'s arguments and let user to enter the arguments, then return the argument list args"""
        args = []
        arguments = inspect.getfullargspec(self.task_options[task_prompt][1]).args
        arg_types = inspect.getfullargspec(self.task_options[task_prompt][1]).annotations

        if arg_types != {}:
            for arg in arguments:
                if arg == 'self':
                    continue
                # argument value passed by user
                passed_arg = input(arg + "(" + str(arg_types[arg].__name__) + "): ")
                # convert argument's type as required
                if arg_types[arg] in [list, bool]:
                    converted_arg = eval(passed_arg)
                else:
                    converted_arg = arg_types[arg](passed_arg)

                args.append(converted_arg)
        return args

    def main_loop(self):
        task_loop = False
        while True:
            print("#" * 80)
            print("#" + "".center(78, " ") + "#")
            print("#" + "".center(78, " ") + "#")
            print("#" + "Welcome to wildfire Task Manager".center(78, " ") + "#")
            print("#" + "Update: Bind task options to task_manager class".center(78, " ") + "#")
            print("#" + "Version 0.2".center(78, " ") + "#")
            print("#" + "Credit to Unicorn".center(78, " ") + "#")
            print("#" + "".center(78, " ") + "#")
            print("#" + "".center(78, " ") + "#")
            print("#" * 80)

            # Clear finished thread
            self.free_dead()
            print("You have following task running in loop: ")
            for i, thread in enumerate(self.running_threads):
                if thread[2]:
                    print("[%d]: %s" % (i, thread[1]))
            print("\nEnter the task Number to stop the task:")
            try:
                stop_task_prompt = input("(if you don't want to break the loop, enter anything else to continue)\n")
                stop_task_prompt = int(stop_task_prompt)
                self.stop_loop(self.running_threads[stop_task_prompt][1])
            except:
                print("Skipped, no task been terminated\n ")
            task_prompt = input("Which task would you like to run:\n" + self.task_option_to_string() + " [q]: quit\n")
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
                task_loop = True
                interval_prompt = input("Interval between each run enter a NUMBER of seconds:\n")
            elif loop_prompt == 'n':
                interval_prompt = 0
            try:
                interval_prompt = int(interval_prompt)
                args = self.pass_arguments(task_prompt)
                self.run(task_option_id=task_prompt, loop=task_loop, interval=interval_prompt, args=args)
                # Increment number of user specified task
                self.task_options[task_prompt][2] += 1
                print("Your task is running!")
            except Exception:
                logger.error('error: ' + traceback.format_exc())
                print("[Error] Your input is not all correct, the task has not started")


if __name__ == "__main__":
    logger = TaskManager.initialize_logger()
    logger.info('Task manager is running now!')
    try:
        task_manager = TaskManager()
        task_manager.main_loop()
    except:
        logger.error('Invalid Input Cause Error')

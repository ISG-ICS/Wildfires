import ctypes
import inspect
import json
import logging.config
import os
import threading
import time
import traceback
from logging import Logger
from typing import Callable, List

import rootpath

rootpath.append()
from paths import LOG_DIR, LOG_CONFIG_PATH

# don't delete these imports because they're called implicitly
exec("from backend.task import *")


class Task:
    def __init__(self, task_name: str, task_func: Callable, task_number: int):
        self.task_name = task_name
        self.task_func = task_func
        self.task_number = task_number


class RunningThread:
    def __init__(self, th, th_name, loop):
        self.th = th
        self.th_name = th_name
        self.loop = loop


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
    running_threads: List[RunningThread] = list()
    task_options = dict()
    # use 'Runnable' as parent class' name and get all the subclasses' names
    for i, sub_cls in enumerate(vars()['Runnable'].__subclasses__()):
        task_options[i + 1] = Task(sub_cls.__name__, sub_cls().run, 1)
    task_option_id = 1

    TASK_MODE = 0
    KILL_MODE = 1
    QUIT_MODE = 2

    def __init__(self):
        self.quit_flag: bool = False
        self.kill_thread_flag: bool = False

    @staticmethod
    def initialize_logger() -> Logger:
        with open(LOG_CONFIG_PATH, 'r') as file:
            # create path to save logs
            if not os.path.exists(LOG_DIR):
                os.makedirs(LOG_DIR)
            config = json.load(file)
            # use json file to config the logger
            logging.config.dictConfig(config)
            logger = logging.getLogger('TaskManager')
            info_format = '[%(asctime)s] [%(levelname)s] [%(threadName)s] [%(module)s] ' \
                          '[%(funcName)s]: %(message)s'
            date_format = '%m/%d/%Y-%H:%M:%S'
            formatter = logging.Formatter(fmt=info_format, datefmt=date_format)
            handler_names = ['info.log', 'error.log']
            current_time = time.strftime('%m%d%Y_%H:%M:%S_', time.localtime(time.time()))
            for handler_name in handler_names:
                file_name = os.path.join(LOG_DIR, current_time + handler_name)
                # create log file in advance
                if not os.path.exists(file_name):
                    os.system(r"touch {}".format(file_name))
                file_handler = logging.FileHandler(file_name, mode='a', encoding=None, delay=False)
                file_handler.setLevel(
                    logging.DEBUG if 'info' in handler_name else logging.ERROR)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        return logger

    @classmethod
    def add_task_option(cls, task_name: str, task_func: Callable, task_number: int) -> None:
        """
        :param task_name: name of this task option
        :param task_func: the runnable of this task
        :param task_number: id of this next task eg. let's say we had a wind_crawler-1 is running, to make our second
                            wind crawler's name unique
                            we increment this number, so next wind crawler task will be called wind_crawler-2
        :return: None
        """
        cls.task_options[cls.task_option_id] = Task(task_name, task_func, task_number)
        cls.task_option_id += 1

    @classmethod
    def delete_task_option(cls, task_option_id: int) -> None:
        """
        :param task_option_id: id of task option you want to delete
        """
        cls.task_options.pop(task_option_id)

    @classmethod
    def task_option_to_string(cls) -> str:
        """
        :return: formated tasks in the current task option dictionary
        """
        to_return = ""
        task_template = " [%d]: %s-%d \n"
        for option in cls.task_options:
            to_return += task_template % (
                option, cls.task_options[option].task_name, cls.task_options[option].task_number)
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
        th_name = cls.task_options[task_option_id].task_name + str(cls.task_options[task_option_id].task_number)
        th = threading.Thread(target=cls._thread_runner_,
                              args=(cls.task_options[task_option_id].task_func, th_name, interval, args),
                              name=th_name)
        logger.info('A new task will be running!')
        th.setDaemon(True)
        cls.running_threads.append(RunningThread(th, th_name, loop))
        th.start()

    @classmethod
    def free_dead(cls):
        """Removes all threads that return FALSE on isAlive() from the running_threads list """
        for running_th in cls.running_threads[:]:
            if not running_th.th.isAlive():
                cls.running_threads.remove(running_th)

    @classmethod
    def stop_thread(cls, thread_name):
        """Stops a looping function that was started with ThM.run(...)"""
        for i, thlis in enumerate(cls.running_threads):
            if thlis.th_name == thread_name:
                exc = ctypes.py_object(SystemExit)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
                    ctypes.c_long(cls.running_threads[i].th.ident), exc)
                if res == 0:
                    raise ValueError("nonexistent thread id")
                elif res > 1:
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(cls.running_threads[i].th.ident, None)
                    raise SystemError("PyThreadState_SetAsyncExc failed")
                logger.info('TASK ' + str(cls.running_threads[i].th_name) + ' KILLED!')
                cls.running_threads.remove(cls.running_threads[i])
                break

    @classmethod
    def join_all(cls):
        """Joins all the threads together into the calling thread."""
        for running_th in cls.running_threads[:]:
            while running_th.th.isAlive():
                time.sleep(0.1)
            running_th.th.join()

    # This method is only intended for threads started with ThM !
    @classmethod
    def _thread_runner_(cls, target_func, th_name, interval, args):
        """Internal function handling the running and looping of the threads
        Note: threading.Event() has not been taken into consideration and neither the
        other thread managing objects (semaphores, locks, etc.)"""
        try:
            # index_ = 0
            # if th_name in [thread_.th_name for thread_ in cls.running_threads]:
            #     index_ += 1

            while True:
                logger.info('TASK ' + th_name + ' START!')

                # log error when worker crashed
                try:
                    target_func(*args)
                except:
                    logger.error("error: " + traceback.format_exc())

                # 'END' means returned or crashed
                logger.info('TASK ' + th_name + ' END!')
                # whether a loop work?

                index_ = None
                for i, thread_ in enumerate(cls.running_threads):
                    if cls.running_threads[i].th_name == th_name:
                        index_ = i

                if index_ is not None and index_ < len(cls.running_threads):
                    if not cls.running_threads[index_].loop:
                        break
                    if interval != 0:
                        time.sleep(interval)
                else:
                    break

        except:
            logger.error("error: " + traceback.format_exc())

    def pass_arguments(self, task_prompt):
        """get function run()'s arguments and let user to enter the arguments, then return the argument list args"""
        args = []
        arg_spec = inspect.getfullargspec(self.task_options[task_prompt].task_func)
        arguments = arg_spec.args
        arg_types = arg_spec.annotations
        arg_default = arg_spec.defaults
        if arg_types != {}:
            for i, arg in enumerate(arguments):
                if arg == 'self':
                    continue
                # argument value passed by user
                passed_arg = input(
                    arg + "(" + str(arg_types[arg].__name__) + ", default: " + str(arg_default[i - 1]) + "): ")
                if passed_arg == "":
                    # use the default value, the default value set doesn't include self, so use i-1 instead
                    converted_arg = arg_default[i - 1]
                # convert argument's type as required

                elif arg_types[arg] in (list, bool):

                    converted_arg = eval(passed_arg)
                else:
                    converted_arg = arg_types[arg](passed_arg)

                args.append(converted_arg)
        return args

    def main_loop(self):
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

        while True:
            # Clear finished thread
            self.free_dead()
            selected_task, task_mode = self.task_selection()
            if task_mode == TaskManager.KILL_MODE:
                self.kill_a_thread()
            elif task_mode == TaskManager.QUIT_MODE:
                print("bye bye")
                break
            else:
                self.run_a_task(selected_task)

    def run_a_task(self, task_prompt):
        while True:
            loop_prompt = self.lower_case_prompt(
                "Would you like to run task in a loop? yes/no ([y]/[n])  ([r] for selecting another task)\n")
            if loop_prompt == 'y':
                task_loop = True
                interval_prompt = self.lower_case_prompt("Interval between each run enter a NUMBER of seconds:\n")
            elif loop_prompt == 'n':
                task_loop = False
                interval_prompt = 0
            elif loop_prompt == 'r':
                break
            else:
                continue
            try:
                args = self.pass_arguments(task_prompt)
                self.run(task_option_id=task_prompt, loop=task_loop, interval=int(interval_prompt), args=args)
                # Increment number of user specified task
                self.task_options[task_prompt].task_number += 1
                print("Task " + str(self.task_options[task_prompt].task_name) + " has been started!\n")
                break
            except:
                print("Your input is not all correct, the task has not started, please try again")
                continue

    @staticmethod
    def lower_case_prompt(message: str) -> str:
        return input(message).strip().lower()

    def kill_a_thread(self):
        print("You have following tasks running: ")
        for i, thread in enumerate(self.running_threads):
            print(f"{i}: {thread.th_name}")
        print("\nEnter the task Number to stop the task:")
        try:
            stop_task_prompt = self.lower_case_prompt(
                "(if you don't want to kill any thread, enter anything else to continue)\n")
            running_thread = self.running_threads[int(stop_task_prompt)]
            self.stop_thread(running_thread.th_name)
            print("Task " + str(running_thread.th_name) + " has been stopped!\n")
        except:
            print("Skipped, no task been terminated\n ")

    def task_selection(self) -> (int, int):
        selected_task = None
        while not selected_task:
            print("You have following task running: ")
            for i, thread in enumerate(self.running_threads):
                print(f"{i}: {thread.th_name}")
            self.kill_thread_flag = False  # flag to kill thread
            self.quit_flag = False  # flag to terminate the TaskManager
            try:
                task_prompt = self.lower_case_prompt(
                    "\nWhich task would you like to run:\n" + self.task_option_to_string()
                    + " [k]: kill a running thread\n [q]: QUIT\n")
                if task_prompt == 'k':
                    return None, TaskManager.KILL_MODE
                elif task_prompt == 'q':
                    if self.lower_case_prompt("Are you sure you want to quit? [Y/N]") not in ['y', 'yes']:
                        continue
                    return None, TaskManager.QUIT_MODE
                else:
                    selected_task = int(task_prompt)
                    # to test whether this is a legal task
                    inspect.getfullargspec(self.task_options[selected_task].task_func)
                    return selected_task, TaskManager.TASK_MODE
            except:
                selected_task = None
                continue


if __name__ == "__main__":
    logger = TaskManager.initialize_logger()
    logger.info('Task manager is running now!')
    try:
        task_manager = TaskManager()
        task_manager.main_loop()
    except:
        logger.error('Invalid Input Cause Error')

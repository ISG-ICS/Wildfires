"""
@author: Yang Cao, Tingxuan Gu, Yichi Zhang
This file contains following classes: Task, RunningThread, TaskManager
"""
import ctypes
import glob
import importlib
import inspect
import json
import logging.config
import os
import threading
import time
import traceback
from logging import Logger
from typing import Callable, List, Dict

import rootpath

rootpath.append()
from paths import LOG_DIR, LOG_CONFIG_PATH, TASK_DIR



# don't delete these imports because they're called implicitly
# exec("from backend.task import *")


class Task:
    """
    This class defines a task, including the name of it and the function it provides
    the number indicates how many tasks of this kind have been run before
    """

    
    def __init__(self, task_name: str, task_func: Callable):
        self.task_name = task_name
        self.task_func = task_func
        self.used_number = list()  # register which numbers has been used

    def get_next_number(self) -> int:
        """Gets minimum available number"""
        for v in range(1, 100):
            if v not in self.used_number:
                return v


class RunningThread:
    """
    This class defines a running thread, including the thread object and the name of it
    'loop' means whether this thread is running in a loop or not
    """

    def __init__(self, th, th_name, task_option_id, given_number, loop):
        self.th = th
        self.th_name = th_name
        self.task_option_id = task_option_id  # we need these 2 field to refer to Task
        self.given_number = given_number  # we need these 2 field to refer to Task
        self.loop = loop


class TaskManager:
    """
    TM (TaskManager)
    This class handles very simple thread operations:
        Reading available tasks from the folder and providing options for user to choose
        Creating single-shot threads -> TM.run(...)
        Creating 'looping per interval' threads -> TM.run(...) with loop set to True
        Joins all the threads together into the calling thread -> TM.join_all()
        Stopping threads based on name -> TM.stop_thread(...)
        Removing stopped threads from 'running_threads' - > TM.free_dead()

    The class has been designed for very simple operations, mainly
    for programs that need "workers" that mindlessly loop over a function

    NOTE: Locks,Events,Semaphores etc. have not been taken into consideration
    and may cause unexpected behaviour if used!
    """

    exec("from backend.task.runnable import Runnable")
    running_threads: List[RunningThread] = list()
    task_options: Dict[int, Task] = dict()
    task_option_id = 1

    TASK_MODE = 0
    KILL_MODE = 1
    QUIT_MODE = 2
    RELOAD_MODE = 3

    @classmethod
    def load_runnables(cls):
        """
        Loads runnables from 'task' directory
        Tasks should be stored in relative path 'task'
        :return:
        """

        exec("from backend.task.runnable import Runnable")
        # TODO: remove existing modules

        # find tasks
        task_dir = TASK_DIR

        tasks = [os.path.split(file)[-1].strip(".py").strip("./")
                 for file in glob.glob(os.path.join(task_dir, './*.py'))]

        # load tasks, add to task_options
        TaskManager.task_options = dict()
        for t in tasks:
            importlib.import_module(f'task.{t}')
        # use 'Runnable' as parent class' name and get all the subclasses' names
        for i, sub_cls in enumerate(vars()['Runnable'].__subclasses__()):
            cls.task_options[i + 1] = Task(sub_cls.__name__, sub_cls().run)

    def __init__(self):
        self.quit_flag: bool = False
        self.kill_thread_flag: bool = False
        TaskManager.load_runnables()

    @staticmethod
    def initialize_logger() -> Logger:
        """
        Initializes a logger
        :return: initialized logger for the task manager
        """
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
            current_time = time.strftime('%m%d%Y_%H-%M-%S_', time.localtime(time.time()))
            for handler_name in handler_names:
                file_name = os.path.join(LOG_DIR, current_time + handler_name)
                # create log file in advance
                if not os.path.exists(file_name):
                    # `touch` only works on *nix systems, not cross-platform. using open()
                    with open(file_name, 'w'):
                        pass
                file_handler = logging.FileHandler(file_name, mode='a', encoding=None, delay=False)
                file_handler.setLevel(
                    logging.DEBUG if 'info' in handler_name else logging.ERROR)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
        return logger

    @classmethod
    def add_task_option(cls, task_name: str, task_func: Callable) -> None:
        """
        Adds a task option
        :param task_name: name of this task option
        :param task_func: the runnable of this task
        (DEPRECATED):param task_number: id of this next task eg. let's say we had a wind_crawler-1 is running, to make our second
                            wind crawler's name unique
                            we increment this number, so next wind crawler task will be called wind_crawler-2
        :return: None
        """
        cls.task_options[cls.task_option_id] = Task(task_name, task_func)
        cls.task_option_id += 1

    @classmethod
    def delete_task_option(cls, task_option_id: int) -> None:
        """
        Deletes a task option
        :param task_option_id: id of task option you want to delete
        """
        cls.task_options.pop(task_option_id)

    @classmethod
    def task_option_to_string(cls) -> str:
        """
        Changes all the task options to strings
        :return: formatted tasks in the current task option dictionary
        """
        to_return = ""
        for option in cls.task_options:
            to_return += f" [{option}]: {cls.task_options[option].task_name}-" \
                         f"{cls.task_options[option].get_next_number()} \n"
        return to_return

    @classmethod
    def run(cls, task_option_id, loop, interval, args=None) -> None:
        """
        Starts a thread to run a selected task, the exception will be caught in `run_a_task()`
        :param task_option_id: task id for task in the task option list
        :param loop:  determine is this is a looped task
        :param interval: time between each execution of the looped task
        :param args: argument for the task
        :return: None
        """

        if args is None:
            args = []
        th_name = cls.task_options[task_option_id].task_name + str(cls.task_options[task_option_id].get_next_number())
        th = threading.Thread(target=cls._thread_runner_,
                              args=(cls.task_options[task_option_id].task_func, th_name, interval, args),
                              name=th_name)
        logger.info('A new task will be running!')
        th.setDaemon(True)
        cls.running_threads.append(RunningThread(th, th_name, task_option_id,
                                                 cls.task_options[task_option_id].get_next_number(), loop))
        # register task number
        cls.task_options[task_option_id].used_number.append(cls.task_options[task_option_id].get_next_number())
        th.start()

    @classmethod
    def free_dead(cls) -> None:
        """Removes all threads that return FALSE on isAlive() from the running_threads list """
        for running_th in cls.running_threads[:]:
            if not running_th.th.isAlive():
                # un-register task number
                cls.task_options[running_th.task_option_id].used_number.remove(running_th.given_number)
                cls.running_threads.remove(running_th)

    @classmethod
    def stop_thread(cls, thread_name) -> None:
        """
        Stops a function that was started with TM.run(...)
        the exception will be caught in kill_a_thread()
        """
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
                # un-register task number
                cls.task_options[cls.running_threads[i].task_option_id] \
                    .used_number.remove(cls.running_threads[i].given_number)
                cls.running_threads.remove(cls.running_threads[i])
                break

    @classmethod
    def join_all(cls) -> None:
        """Joins all the threads together into the calling thread"""
        for running_th in cls.running_threads[:]:
            while running_th.th.isAlive():
                time.sleep(0.1)
            running_th.th.join()

    # This method is only intended for threads started with TM !
    @classmethod
    def _thread_runner_(cls, target_func, th_name, interval, args) -> None:
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

    def pass_arguments(self, task_prompt) -> list:
        """
        Gets function run()'s arguments and let user to enter the arguments, then return the argument list args
        the exception will be caught in run_a_task()
        """
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

    def main_loop(self) -> None:
        """
        The main function to run the task manager
        the exception will be caught in the main()
        """
        print("#" * 80)
        print("#" + "".center(78, " ") + "#")
        print("#" + "".center(78, " ") + "#")
        print("#" + "Welcome to wildfire Task Manager".center(78, " ") + "#")
        print("#" + "Version 1.0".center(78, " ") + "#")
        print("#" + "Credit to Unicorn, Tingxuan Gu, Yichi Zhang".center(78, " ") + "#")
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
            elif task_mode == TaskManager.RELOAD_MODE:

                TaskManager.load_runnables()
                continue
            else:
                self.run_a_task(selected_task)

    def run_a_task(self, task_prompt) -> None:
        """
        The exception will be caught in main()
        :param task_prompt: the id of the task that user wants to start
        :return: None
        """
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
                print("Task " + str(self.task_options[task_prompt].task_name) + " has been started!\n")
                break
            except:
                print("Your input is not all correct, the task has not started, please try again")
                continue

    @staticmethod
    def lower_case_prompt(message: str) -> str:
        """
        Makes the message into a lower case one
        The exception will be caught in kill_a_thread() and task_selection()
        """
        return input(message).strip().lower()

    def kill_a_thread(self) -> None:
        """
        Provides the user with the running threads and user can choose one to kill
        the exception will be caught in main()
        """
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
        """
        Provides user with choices and user can choose to run/kill a thread or quit the task manager
        the exception will be caught in main()
        :return: selected task's number(str/None), task mode(task, kill or quit)
        """
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
                    + " [k]: kill a running thread\n [q]: QUIT\n [r]: Reload\n")
                if task_prompt == 'k':
                    return None, TaskManager.KILL_MODE
                elif task_prompt == 'q':
                    if self.lower_case_prompt("Are you sure you want to quit? [Y/N]") not in ['y', 'yes']:
                        continue
                    return None, TaskManager.QUIT_MODE
                elif task_prompt == 'r':
                    return None, TaskManager.RELOAD_MODE
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
    logger.addHandler(logging.StreamHandler())
    logger.info('Task manager is running now!')
    try:
        task_manager = TaskManager()
        task_manager.main_loop()
    except:
        logger.error('Invalid Input Cause Error')

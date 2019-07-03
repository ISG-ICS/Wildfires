import errno
import os
import signal
from functools import wraps

import requests


class TimeoutError(Exception):
    def __init__(self, value="Timed Out"):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TimeoutException(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutException(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


class URLClassifier:
    TWEET_IMAGE = 0
    TWEET_VIDEO = 1
    INS = 2
    OTHERS = 3

    @timeout(5)
    def classify(self, short_link):
        # function returns the type of the link, 3 is tweet, 4 is ins, 5 is others
        expanded_url = requests.get(short_link).url
        print(expanded_url)
        if (expanded_url.find("twitter") != -1) and (expanded_url.find("instagram") == -1):
            if expanded_url.find("video") != -1:
                return 1
            else:
                return 0
        elif expanded_url.find("instagram") != -1:
            return 2
        else:
            return 3

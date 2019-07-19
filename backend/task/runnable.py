from abc import ABC, abstractmethod


class Runnable(ABC):
    """ Base class for Runnable.
    """

    @abstractmethod
    def run(self, *args, **kwargs):
        pass

from abc import ABC, abstractmethod
from typing import Union, List, Dict


class DumperException(Exception):
    pass


class DumperBase(ABC):
    def __init__(self):
        super().__init__()
        self.inserted_count = 0
        # dumper holds no data in memory

    @abstractmethod
    def insert(self, data: Union[List, Dict], *args, **kwargs):
        # insert record into database
        # recording insert count number to self.inserted_count
        pass

    def report_status(self):
        return self.inserted_count

    def __str__(self):
        return f'{self.__class__.__name__}{{inserted={self.inserted_count}}}'

    __repr = __str__

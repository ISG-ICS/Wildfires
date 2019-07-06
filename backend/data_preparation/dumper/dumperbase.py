from abc import ABC, abstractmethod


class DumperBase(ABC):
    def __init__(self):
        super().__init__()
        self.inserted_count = 0
        # dumper holds no data in memory

    @staticmethod
    @abstractmethod
    def insert_one(*args, **kwargs):
        # insert one record into database
        # recording insert count number to self.inserted_count
        pass

    @staticmethod
    @abstractmethod
    def insert_batch(*args, **kwargs):
        # insert a batch of records into database
        # recording insert count number to self.inserted_count
        pass

    def report_status(self):
        return self.inserted_count

    def __str__(self):
        return f'{self.__class__.__name__}{{inserted={self.inserted_count}}}'

    __repr = __str__

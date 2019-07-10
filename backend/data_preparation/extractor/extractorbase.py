from abc import ABC, abstractmethod
from typing import Dict, Union, List


class ExtractorException(Exception):
    pass


class ExtractorBase(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.data: Union[List, Dict, None] = None

    @abstractmethod
    def extract(self, *args, **kwargs) -> Union[List, Dict]:
        pass

    @abstractmethod
    def export(self, file_type: str, file_name: str) -> None:  # json
        pass

    def __getitem__(self, index):
        return self.data[index]

    def __str__(self):
        return f'{self.__class__.__name__}'

    def __iter__(self):
        return iter(self.data.items())

    __repr = __str__

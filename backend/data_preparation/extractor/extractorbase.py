from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple


class ExtractorBase(ABC):
    def __init__(self, filename: str):
        super().__init__()
        self.data: Dict = dict()
        self.filename: str = filename

    @abstractmethod
    def extract(self, *args, **kwargs):
        pass

    @abstractmethod
    def export(self, file_type: str, file_name: str) -> None:  # json
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

    def __str__(self):
        return f'{self.__class__.__name__}{{filename={self.filename}}}'

    def __iter__(self):
        return iter(self.data.items())

    __repr = __str__

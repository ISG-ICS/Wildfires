from abc import ABC, abstractmethod
from typing import Dict, Union, List

import numpy as np


class CrawlerBase(ABC):
    def __init__(self):
        super().__init__()
        self.data: Union[List, Dict, None] = None

    @abstractmethod
    def crawl(self, *args, **kwargs) -> Union[List, Dict, np.array]:
        # saves the crawled data to self.data (in-memory), or, if needed, to disk file.
        # also returns a reference of self.data
        pass

    def __getitem__(self, index):
        # get item from in-memory structure self.data
        return self.data[index]

    def __str__(self):
        return f'{self.__class__.__name__}'

    __repr__ = __str__

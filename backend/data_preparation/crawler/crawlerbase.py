from abc import ABC, abstractmethod
from typing import Dict, Union, Optional, List

import rootpath

rootpath.append()
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.extractor.extractorbase import ExtractorBase


class CrawlerBase(ABC):
    def __init__(self, extractor: ExtractorBase = None, dumper: DumperBase = None):
        super().__init__()
        self.data: Union[List, Dict, None] = None
        self.extractor: Optional[ExtractorBase] = extractor
        self.dumper: Optional[DumperBase] = dumper

    def set_extractor(self, extractor: ExtractorBase):
        self.extractor = extractor

    def set_dumper(self, dumper: DumperBase):
        self.dumper = dumper

    @abstractmethod
    def crawl(self, *args, **kwargs) -> Union[List, Dict]:
        # save crawled to self.data (in-memory), or, if needed, to disk file
        # also return a reference of self.data
        pass

    def __getitem__(self, index):
        # get item from in-memory structure self.data
        return self.data[index]

    def __str__(self):
        return f'{self.__class__.__name__}'

    __repr = __str__

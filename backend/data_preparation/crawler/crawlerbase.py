from abc import ABC, abstractmethod
from typing import Dict, Union, Optional, List

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.extractor.extractorbase import ExtractorBase


class CrawlerBase(ABC):
    def __init__(self, extractor: ExtractorBase = None, dumper: DumperBase = None):
        super().__init__()
        self.data: Union[List, Dict]
        self.dumper: Optional[DumperBase] = None
        self.inject_dumper(dumper)
        self.extractor: Optional[ExtractorBase] = None
        self.inject_extractor(extractor)

    def inject_extractor(self, extractor: ExtractorBase):
        self.extractor = extractor

    def inject_dumper(self, dumper: DumperBase):
        self.dumper = dumper

    @abstractmethod
    def start(self, end_clause=None, *args, **kwargs):
        # start crawling information to in-memory structure self.data

        # call extractor to extract from self.data

        # call dumper to data from self.data to database

        # until it reaches the end_clause

        pass

    @abstractmethod
    def __getitem__(self, index):
        # get item from in-memory structure self.data
        pass

    def __str__(self):
        return f'{self.__class__.__name__}'

    __repr = __str__

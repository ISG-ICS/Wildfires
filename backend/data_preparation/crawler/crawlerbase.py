from abc import ABC, abstractmethod
from typing import Dict, Union, Optional, List

import rootpath

rootpath.append()
from backend.data_preparation.dumper.dumperbase import DumperBase, DumperException
from backend.data_preparation.extractor.extractorbase import ExtractorBase, ExtractorException


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

    @abstractmethod
    def start(self, end_clause=None, *args, **kwargs) -> None:

        # TODO: This function is meant to be as
        # verify if both extractor and dumper are set up, raise ExtractorException or DumperException respectively
        if not self.extractor:
            raise ExtractorException
        if not self.dumper:
            raise DumperException

        # until it reaches the end_clause
        while not end_clause:
            # start crawling information to in-memory structure self.data
            raw_data = self.crawl()

            # call extractor to extract from self.data
            extracted_data = self.extractor.extract(raw_data)

            # call dumper to data from self.data to database
            self.dumper.insert(extracted_data)

    def __getitem__(self, index):
        # get item from in-memory structure self.data
        return self.data[index]

    def __str__(self):
        return f'{self.__class__.__name__}'

    __repr = __str__

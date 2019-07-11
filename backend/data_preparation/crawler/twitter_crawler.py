import re
import string
from typing import List, Set, Union, Dict
import rootpath

rootpath.append()

import requests
import twitter
import time

from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.dumper.twitter_dumper import TweetDumper
from backend.data_preparation.extractor.twitter_extractor import TweetExtractor
from backend.data_preparation.dumper.dumperbase import DumperBase, DumperException
from backend.data_preparation.extractor.extractorbase import ExtractorBase, ExtractorException

# TODO import twitter API account information

api = twitter.Api(consumer_key="",
                  consumer_secret="",
                  access_token_key="",
                  access_token_secret="")


class TweetCrawler(CrawlerBase):

    def __init__(self, extractor: ExtractorBase = None, dumper: DumperBase = None):
        super().__init__(extractor, dumper)
        self.data = []
        self.keywords = []
        self.total_crawled_count = 0

    def start(self, keywords: List[str], batch_number: int, end_clause=None) -> None:
        self.keywords = keywords

        if not self.extractor:
            raise ExtractorException('Extractor not found')
        if not self.dumper:
            raise DumperException('Dumper not found')

        # TODO: check for exceptions raised from extractor and dumper

        # until it reaches the end_clause
        while not end_clause:
            # starts crawling information to in-memory structure self.data
            self.crawl(self.keywords, batch_number)
            self.total_crawled_count += len(self.data)


            # call extractor to extract from self.data
            extracted_data = self.extractor.extract(self.data)
            # calls dumper to data from self.data to database
            self.dumper.insert(extracted_data)



    def crawl(self, keywords: List, batch_number) -> Union[Dict, List]:
        """crawl the tweets and save them into self.data"""

        id_set = self._crawl_tweet_ids()

        while len(id_set) < batch_number:
            # loops until the number of id collected is greater than the batch number
            id_set.update(self._crawl_tweet_ids())

        # gets status with the list that has batch# (can be a bit more than the batch#) amount of tweets
        self.data = api.GetStatuses(id_set)

        # save crawled to self.data (in-memory), or, if needed, to disk file
        # also return a reference of self.data
        return self.data

    def _crawl_tweet_ids(self) -> Set[int]:
        """helper function for crawling tweets, collecting all tweet ids"""

        ids = set()
        for keyword in self.keywords:
            # allows the input to be a keyword list
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/72.0.3626.121 Safari/537.36 '
            }  # Simulates request from a mac browser
            resp = requests.get(
                f'https://twitter.com/i/search/timeline?f=tweets&vertical=news&q={keyword}%20near%3A\"United%20States'
                f'\"%20within%3A8000mi&l=en&src=typd', headers=headers)

            # Clears all punctuation from raw response body
            content = str(resp.content).translate(str.maketrans("", "", string.punctuation))

            ids.update(re.findall("dataitemid(\d+)", content))

        return ids


if __name__ == '__main__':
    t0 = time.time()

    crawler = TweetCrawler(TweetExtractor(), TweetDumper())

    # crawler = TweetCrawler()
    # crawler.set_dumper(TweetDumper())
    # crawler.set_extractor(TweetExtractor())

    crawler.start(['wildfire'], 20, end_clause=None)
    t = time.time()
    timeCounted = t - t0

    print('time:', timeCounted)

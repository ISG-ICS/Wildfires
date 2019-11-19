import logging
import re
import string
import time
import traceback
from typing import List, Set

import requests
import rootpath
import twitter

rootpath.append()

from paths import TWITTER_API_CONFIG_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.utilities.ini_parser import parse
from backend.utilities.cacheset import CacheSet

logger = logging.getLogger('TaskManager')


class TweetSearchAPICrawler(CrawlerBase):
    MAX_WAIT_TIME = 64

    def __init__(self):
        super().__init__()
        self.wait_time = 1
        self.api = twitter.Api(**parse(TWITTER_API_CONFIG_PATH, 'twitter-API'))
        self.data = []
        self.keywords = []
        self.total_crawled_count = 0
        self.cache: CacheSet[int] = CacheSet()
        self.data_from_db_count = 0

    def crawl(self, keywords: List, batch_number: int) -> List[int]:
        """
        Crawling Tweet ID with the given keyword lists, with searching on www.twitter.com

        It is hard to parse all information from the returned html of searching, thus using regex to get Tweet IDs only.

        Args:

            keywords (List[str]): keywords that to be used for keyword search of tweet text, hash-tag, etc.

            batch_number (int): a number that limits the returned list length. using 100 as default since Twitter API
                limitation is set to 100 IDs per request.


        Returns:
             (List[int]): a list of Tweet IDs

        """
        self.keywords = keywords
        logger.info(f'Crawler Started')

        # crawl tweet ids
        crawled_ids = self._crawl_tweet_ids()
        logger.info(f"Crawled ID count in this batch: {len(crawled_ids)}")

        # gets status with the list that has batch number (can be a bit more than the batch#) amount of tweets
        while len(crawled_ids) < batch_number:
            # loops until the number of id collected is greater than the batch number
            current_count = len(crawled_ids)
            time.sleep(0.1)
            crawled_ids.extend(self._crawl_tweet_ids())
            if len(crawled_ids) > current_count:
                logger.info(f"Crawled ID count in this batch: {len(crawled_ids)}")
        logger.info(f'Outputting {len(crawled_ids)} Tweet IDs')

        # turn ids into list of dict and turn each dict into Status
        self.data = list(crawled_ids)
        self.total_crawled_count += len(crawled_ids)
        crawled_ids.clear()
        logger.info(f'Total crawled count {self.total_crawled_count}')
        return list(self.data)

    def _crawl_tweet_ids(self) -> List[int]:
        """helper function for crawling tweets, collecting all tweet ids"""

        ids: Set[int] = set()

        for keyword in self.keywords:
            # allows the input to be a keyword list
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/72.0.3626.121 Safari/537.36 '
            }  # Simulates request from a mac browser
            try:
                resp = requests.get(
                    f'https://twitter.com/i/search/timeline?f=tweets&vertical=news&q={keyword}%20near%3A\"United%20States'
                    f'\"%20within%3A8000mi&l=en&src=typd', headers=headers)

            except requests.exceptions.RequestException:
                logger.error('error: ' + traceback.format_exc())
                continue
                # Clears all punctuation from raw response body
            content = str(resp.content).translate(str.maketrans("", "", string.punctuation))
            ids.update(map(int, re.findall("dataitemid(\d+)", content)))

        return self._filter(ids)

    def _filter(self, ids: Set[int]) -> List[int]:
        """using self.cache to filter out duplicates"""
        unique_ids = list(filter(lambda i: i not in self.cache, ids))
        self.cache.update(unique_ids)
        return unique_ids


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    tweet_search_api_crawler = TweetSearchAPICrawler()

    for _ in range(10):
        raw_tweets = tweet_search_api_crawler.crawl(['fire'], batch_number=100)
        print(raw_tweets)

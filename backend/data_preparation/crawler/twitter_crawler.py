import logging
import re
import string
import time
import traceback
from typing import List, Set, Union, Dict

import requests
import rootpath
import twitter

rootpath.append()

from paths import TWITTER_API_CONFIG_PATH
from backend.connection import Connection
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.utilities.ini_parser import parse

logger = logging.getLogger('TaskManager')


class TweetCrawler(CrawlerBase):

    def __init__(self):
        super().__init__()
        self.api = twitter.Api(**parse(TWITTER_API_CONFIG_PATH, 'twitter-API'))
        self.data = []
        self.keywords = []
        self.total_crawled_count = 0
        self.crawled_id_set: Set[int] = set()
        self.data_from_db_count = 0

    def crawl(self, keywords: List, batch_number: int, fetch_from_db: bool) -> Union[Dict, List]:
        """crawl the tweets and save them into self.data"""
        self.keywords = keywords
        if not fetch_from_db:
            # crawl status ids
            logger.info(f"Online Mode: Total crawled count {self.total_crawled_count}")
            self.crawled_id_set = self._crawl_tweet_ids()
            logger.info(f"Online Mode: crawled {len(self.crawled_id_set)}")

            while len(self.crawled_id_set) < batch_number:
                # loops until the number of id collected is greater than the batch number
                current_count = len(self.crawled_id_set)
                time.sleep(10)
                self.crawled_id_set.update(self._crawl_tweet_ids())
                if len(self.crawled_id_set) > current_count:
                    logger.info(f"Online Mode: crawled: {len(self.crawled_id_set)}")

            # gets status with the list that has batch number (can be a bit more than the batch#) amount of tweets
            ids = list(self.crawled_id_set)
        else:
            # reprocess the crawled status ids that are stored in db
            ids = next(self.id_generator)
            logger.info(f'DB Mode: ids taken from db length {len(ids)}')
            logger.info(f'DB Mode: Total crawled count {self.total_crawled_count}')
        try:
            self.data = self.api.GetStatuses(ids)
            # reset the set to empty so that the id will not accumulate
            # in the case that the twitter API works
        except Exception:
            logger.error('error: ' + traceback.format_exc())
            # in this case the collected twitter id will be recorded and tried again next time
        else:
            self.crawled_id_set.clear()
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
            try:
                resp = requests.get(
                    f'https://twitter.com/i/search/timeline?f=tweets&vertical=news&q={keyword}%20near%3A\"United%20States'
                    f'\"%20within%3A8000mi&l=en&src=typd', headers=headers)

            except requests.exceptions.RequestException:
                logger.error('error: ' + traceback.format_exc())
                continue
                # Clears all punctuation from raw response body
            content = str(resp.content).translate(str.maketrans("", "", string.punctuation))
            ids.update(re.findall("dataitemid(\d+)", content))

        return ids

    @staticmethod
    def fetch_status_id_from_db():
        """a generator which generates 100 id list at a time"""
        count = 0
        result = list()
        for id, in Connection.sql_execute(f"SELECT id FROM records WHERE user_id IS NULL ORDER BY create_at DESC"):
            count += 1
            result.append(id)
            if count >= 100:
                yield result
                result.clear()
                count = 0


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    # online mode
    raw_tweets = TweetCrawler().crawl(['wildfires'], batch_number=100, fetch_from_db=False)
    print(raw_tweets)

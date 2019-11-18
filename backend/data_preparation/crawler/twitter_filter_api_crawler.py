import logging
import time
import traceback
from typing import List, Set

import rootpath
import twitter

rootpath.append()

from paths import TWITTER_API_CONFIG_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.utilities.ini_parser import parse

logger = logging.getLogger('TaskManager')


class TweetFilterAPICrawler(CrawlerBase):
    MAX_WAIT_TIME = 64

    def __init__(self):
        super().__init__()
        self.wait_time = 1
        self.api = twitter.Api(**parse(TWITTER_API_CONFIG_PATH, 'twitter-API'))
        self.data: List = []
        self.keywords = []
        self.total_crawled_count = 0
        self.crawled_tweet_id_set: Set[int] = set()

    def crawl(self, keywords: List, batch_number: int = 100) -> List[int]:
        """
        Crawling Tweet ID with the given keyword lists, using Twitter Filter API

        Twitter Filter API only provides compatibility mode, thus no `full_text` is returned by the API. Have to crawl
        for IDs and then fetch full_text with GetStatus, which will be in other thread.

        Args:

            keywords (List[str]): keywords that to be used for filtering tweet text, hash-tag, etc. Exact behavior
                is defined by python-twitter.

            batch_number (int): a number that limits the returned list length. using 100 as default since Twitter API
                limitation is set to 100 IDs per request.

        Returns:
             (List[int]): a list of Tweet IDs

        """

        logger.info(f'Crawler Started')
        slice_num = batch_number
        while len(self.crawled_tweet_id_set) < batch_number:
            logger.info(f'Sending a Request to Twitter Filter API')
            try:

                for tweet in self.api.GetStreamFilter(track=keywords):
                    self.reset_wait_time()
                    self.crawled_tweet_id_set.add(tweet['id'])
                    count = len(self.crawled_tweet_id_set)
                    if count % (batch_number // 10) == 0:
                        logger.info(f"Crawled ID count in this batch: {count}")

                    if count > batch_number:
                        break

            except:
                # in this case the collected twitter id will be recorded and tried again next time
                logger.error(f'Error: {traceback.format_exc()}')
                slice_num = len(self.crawled_tweet_id_set)

                self.wait()
            else:
                slice_num = batch_number

        self.data = [self.crawled_tweet_id_set.pop() for _ in range(slice_num)]
        logger.info(f'Outputting {slice_num} Tweet IDs')
        self.total_crawled_count += len(self.data)
        logger.info(f'Total crawled count {self.total_crawled_count}')
        return self.data

    def reset_wait_time(self):
        """resets the wait time"""
        self.wait_time = 1

    def wait(self) -> None:
        """Incrementally waits when the request rate hits limitation."""
        time.sleep(self.wait_time)
        if self.wait_time < self.MAX_WAIT_TIME:  # set a wait time limit no longer than 64s
            self.wait_time *= 2  # an exponential back-off pattern in subsequent reconnection attempts


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    tweet_filter_api_crawler = TweetFilterAPICrawler()
    for _ in range(2):
        raw_tweets = tweet_filter_api_crawler.crawl(['fire'], batch_number=100)
        print(raw_tweets)

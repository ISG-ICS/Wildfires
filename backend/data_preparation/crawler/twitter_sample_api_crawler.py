import logging
import time
import traceback
from typing import List, Set, Union, Dict

import rootpath
import twitter

rootpath.append()

from paths import TWITTER_API_CONFIG_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.utilities.ini_parser import parse

logger = logging.getLogger('TaskManager')


class TweetSampleAPICrawler(CrawlerBase):
    MAX_WAIT_TIME = 64

    def __init__(self):
        super().__init__()
        self.wait_time = 1
        self.api = twitter.Api(**parse(TWITTER_API_CONFIG_PATH, 'twitter-API'))
        self.data = []
        self.keywords = []
        self.total_crawled_count = 0
        self.crawled_tweet_set: Set[twitter.Status] = set()

    def crawl(self, keywords: List, batch_number: int = 100) -> Union[Dict, List]:
        """crawl the tweets and save them into self.data"""
        while len(self.crawled_tweet_set) < batch_number:
            logger.info(f'Crawler Started')
            try:
                for tweet in self.api.GetStreamFilter(track=keywords):
                    self.crawled_tweet_set.add(twitter.Status.NewFromJsonDict(tweet))
                    self.wait_time = 1  # reset the wait time to 1
                    if len(self.crawled_tweet_set) > batch_number:
                        break
            except:
                # in this case the collected twitter id will be recorded and tried again next time
                logger.error(f'Error: {traceback.format_exc()}')
                slice_num = len(self.crawled_tweet_set)

                time.sleep(self.wait_time)
                print(self.wait_time)
                if self.wait_time < self.MAX_WAIT_TIME:  # set a wait time limit no longer than 64s
                    self.wait_time *= 2  # an exponential back-off pattern in subsequent reconnection attempts
            else:
                slice_num = batch_number

            self.data = [self.crawled_tweet_set.pop() for _ in range(slice_num)]
            logger.info(f'Outputting {slice_num} tweets')
            self.total_crawled_count += len(self.data)
            logger.info(f'Total crawled count {self.total_crawled_count}')
            return self.data


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    tweet_sample_api_crawler = TweetSampleAPICrawler()
    for _ in range(20):
        raw_tweets = tweet_sample_api_crawler.crawl(['wildfire'], batch_number=5)
        print(raw_tweets)

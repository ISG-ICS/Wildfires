import logging
import time
import traceback
from typing import List

import rootpath
import twitter
from tokenizer import tokenize, TOK

rootpath.append()

from paths import TWITTER_API_CONFIG_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.utilities.ini_parser import parse
from backend.utilities.cacheset import CacheSet

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
        self.cache: CacheSet[int] = CacheSet()

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
        self.keywords = keywords + ["#" + keyword for keyword in keywords]
        logger.info(f'Crawler Started')
        self.data = []
        while len(self.data) < batch_number:
            logger.info(f'Sending a Request to Twitter Filter API')
            try:

                for tweet in self.api.GetStreamFilter(track=keywords, languages=['en'],
                                                      locations=map(str, [-127.86, 19.55, -55.15, 47.92])):
                    self.reset_wait_time()

                    has_keywords = set(self.keywords) & self._tokenize_tweet_text(tweet)
                    if tweet.get('retweeted_status') and set(self.keywords) & self._tokenize_tweet_text(
                            tweet['retweeted_status']):
                        self._add_to_batch(tweet['retweeted_status']['id'])

                    elif tweet.get('place') and tweet['place']['country_code'] == "US" and has_keywords:
                        self._add_to_batch(tweet['id'])
                    else:
                        continue

                    count = len(self.data)
                    if count % (batch_number // 10) == 0:
                        logger.info(f"Crawled ID count in this batch: {count}")

                    if count >= batch_number:
                        break

            except:
                # in this case the collected twitter id will be recorded and tried again next time
                logger.error(f'Error: {traceback.format_exc()}')
                self.wait()

        count = len(self.data)
        logger.info(f'Outputting {count} Tweet IDs')
        self.total_crawled_count += count
        logger.info(f'Total crawled count {self.total_crawled_count}')
        return self.data

    @staticmethod
    def _tokenize_tweet_text(tweet):
        return set(txt for kind, txt, _ in tokenize(tweet['text']) if kind in [TOK.WORD, TOK.HASHTAG])

    def _add_to_batch(self, tweet_id: int) -> None:
        if tweet_id not in self.cache:
            self.data.append(tweet_id)
            self.cache.add(tweet_id)

    def reset_wait_time(self) -> None:
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
    for _ in range(3):
        raw_tweets = tweet_filter_api_crawler.crawl(['wildfire', 'fire', 'smoke'], batch_number=100)
        print(raw_tweets)

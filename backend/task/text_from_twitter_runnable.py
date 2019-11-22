"""
@author: Tingxuan Gu, Rose Du, Yicong Huang
"""
import logging
import pickle
import time

import rootpath

from paths import TWITTER_TEXT_CACHE

rootpath.append()
from backend.connection import Connection
from backend.utilities.cacheset import CacheSet
from backend.data_preparation.crawler.twitter_filter_api_crawler import TweetFilterAPICrawler
from backend.data_preparation.crawler.twitter_id_mode_crawler import TweetIDModeCrawler
from backend.data_preparation.crawler.twitter_search_api_crawler import TweetSearchAPICrawler
from backend.data_preparation.dumper.twitter_dumper import TweetDumper
from backend.data_preparation.extractor.twitter_extractor import TweetExtractor
from backend.task.runnable import Runnable

logger = logging.getLogger('TaskManager')


class TextFromTwitter(Runnable):
    """
    This class is responsible for crawling texts from twitter, extracting them and dumping them into database
    """

    def __init__(self):
        self.crawler = TweetSearchAPICrawler()
        self.extractor = TweetExtractor()
        self.dumper = TweetDumper()
        try:
            self.cache: CacheSet[int] = pickle.load(open(TWITTER_TEXT_CACHE, 'rb'))
        except:
            self.cache = CacheSet()

    def run(self, keywords: list = None, batch_num: int = 100, using_filter_api: bool = False,
            fetch_from_db: bool = False, time_interval: int = 2):

        if keywords is None:
            keywords = ['wildfire']

        logger.info('Crawler Starting')
        if fetch_from_db:
            return self._run_fetch_from_db_mode(time_interval)

        # crawling ids:
        if using_filter_api and not isinstance(self.crawler, TweetFilterAPICrawler):
            self.crawler = TweetFilterAPICrawler()

        while True:
            fire_names = {fire_name.lower() for fire_name, in Connection.sql_execute(
                f"select name from fire_merged where start_time > now() - interval '1 month'")}
            keywords_with_fire_names = fire_names | (set(keywords))
            logger.info('Running ID mode')
            ids = self.crawler.crawl(list(keywords_with_fire_names), batch_num)
            self.dumper.insert(ids, id_mode=True)

            # prevent API from being banned
            time.sleep(time_interval)

    def _run_fetch_from_db_mode(self, time_interval):
        if not isinstance(self.crawler, TweetIDModeCrawler):
            self.crawler = TweetIDModeCrawler()
        while True:
            logger.info('Running Fetch From DB mode')
            for ids in self._fetch_id_from_db():
                status = self.crawler.crawl(ids)
                tweets = self.extractor.extract(status)
                self.dumper.insert(tweets)

                # prevent API from being banned
                time.sleep(time_interval)
            time.sleep(time_interval)

    def _fetch_id_from_db(self):
        """a generator which generates 100 id list at a time"""
        result = list()
        for id, in Connection.sql_execute(
                f"SELECT id FROM records WHERE user_id IS NULL or text is null ORDER BY create_at DESC"):
            if id not in self.cache:
                self.cache.add(id)
                result.append(id)
            if len(result) == 100:
                yield result
                result.clear()
        pickle.dump(self.cache, open(TWITTER_TEXT_CACHE, 'wb+'))
        yield result


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    # search API mode
    TextFromTwitter().run(keywords=['wildfire'])

    # # filter API mode
    TextFromTwitter().run(keywords=['wildfire'], using_filter_api=True)

    # fetch from db mode
    TextFromTwitter().run(fetch_from_db=True)

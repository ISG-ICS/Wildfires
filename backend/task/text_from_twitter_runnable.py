"""
@author: Tingxuan Gu, Rose Du, Yicong Huang
"""
import logging
import time

import rootpath

rootpath.append()
from backend.connection import Connection
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
            logger.info('Running ID mode')
            ids = self.crawler.crawl(keywords, batch_num)
            self.dumper.insert(ids, id_mode=True)

            # prevent API from being banned
            time.sleep(time_interval)

    def _run_fetch_from_db_mode(self, time_interval):
        if not isinstance(self.crawler, TweetIDModeCrawler):
            self.crawler = TweetIDModeCrawler()
        for ids in self._fetch_id_from_db():
            logger.info('Running Fetch From DB mode')
            status = self.crawler.crawl(ids)
            tweets = self.extractor.extract(status)
            self.dumper.insert(tweets)

            # prevent API from being banned
            time.sleep(time_interval)
        logger.info("Crawler Finished")

    @staticmethod
    def _fetch_id_from_db():
        """a generator which generates 100 id list at a time"""
        count = 0
        result = list()
        for id, in Connection.sql_execute(
                f"SELECT id FROM records WHERE user_id IS NULL or text is null ORDER BY create_at DESC"):
            count += 1
            result.append(id)
            if count >= 100:
                yield result
                result.clear()
                count = 0
        yield result


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    # # search API mode
    TextFromTwitter().run(keywords=['wildfire'])

    # # filter API mode
    TextFromTwitter().run(keywords=['wildfire'], using_filter_api=True)

    # fetch from db mode
    TextFromTwitter().run(fetch_from_db=True)

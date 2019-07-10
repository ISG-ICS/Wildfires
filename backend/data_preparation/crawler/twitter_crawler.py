import re
import string
from typing import List

import rootpath

rootpath.append()

import requests
import twitter
import time

from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.dumper.twitter_dumper import TweetDumper
from backend.data_preparation.extractor.twitter_extractor import TweetExtractor
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.extractor.extractorbase import ExtractorBase

# account info can be found on slack
api = twitter.Api(consumer_key="",
                  consumer_secret="",
                  access_token_key="",
                  access_token_secret="")


class TweetCrawler(CrawlerBase):

    def __init__(self, extractor: ExtractorBase = None, dumper: DumperBase = None):
        super().__init__()
        self.data = []
        self.cnt = 0
        self.keywords = []

    def start(self, keywords, batch_number, end_clause=None):
        self.keywords = keywords

        if not self.extractor:
            raise Exception('Extractor error')
        if not self.dumper:
            raise Exception('Dumper error')

        # until it reaches the end_clause
        while not end_clause:
            # starts crawling information to in-memory structure self.data
            raw_data = self.crawl(self.keywords, batch_number)

            # call extractor to extract from self.data
            extracted_data = self.extractor.extract(raw_data)
            self.extractor.export('json', 'tweets_extractor_export')
            # calls dumper to data from self.data to database
            self.dumper.insert(extracted_data)
            print('(new_records, new_locations)', self.dumper.report_status())

    def tweet_crawler_with_keywords(self):
        # helper function for crawling tweets
        content_list = []
        for keyword in self.keywords:
            # allows the input to be a keyword list

            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
            }  # Simulates request from a mac browser
            resp = requests.get(
                'https://twitter.com/i/search/timeline?f=tweets&vertical=news&q=' + keyword + '%20near%3A\"United%20States\"%20within%3A8000mi&l=en&src=typd',
                headers=headers)
            # Clears all punctuation from raw response body
            tr = str.maketrans("", "", string.punctuation)
            content = str(resp.content)
            content = content.translate(tr)
            content_list.append(content)
        return content_list

    def crawl(self, keywords: List, batch_number):
        cnt = 0
        id_list = []

        while cnt < batch_number:
            # loops until the number of id collected is greater than the batch number
            content_list = self.tweet_crawler_with_keywords()
            for content in content_list:
                for id in re.findall("dataitemid(\d+)", content):
                    if id not in id_list and cnt < batch_number:
                        id_list.append(id)
                        cnt += 1

        returning_list = api.GetStatuses(id_list)
        # gets status with the list that has batch# (can be a bit more than the batch#) amount of tweets
        self.data = returning_list
        return returning_list
        # save crawled to self.data (in-memory), or, if needed, to disk file
        # also return a reference of self.data


if __name__ == '__main__':
    t0 = time.time()
    crawler = TweetCrawler()
    crawler.set_dumper(TweetDumper())
    crawler.set_extractor(TweetExtractor())
    crawler.start(['wildfire'], 20, end_clause=None)
    t = time.time()
    timeCounted = t - t0

    print('time:', timeCounted)

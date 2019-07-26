import os
import sys
import time
from datetime import datetime, timedelta, timezone
import datetime
import rootpath

from paths import FIRE_DATA_DIR

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.crawler.fire_crawler import FireCrawler
from backend.data_preparation.extractor.fire_extractor import FireExtractor
from backend.data_preparation.dumper.fire_dumper import FireDumper




class DataFromNoaa(Runnable):
    """run once per day/week/, not any time"""
    def __init__(self):
        self.crawler = FireCrawler()
        self.extractor = FireExtractor()
        self.dumper = FireDumper()
        self.explored_year = set()
        self.explored_fire = set()




    def run(self):
        """
        Interface for runnable
        """
        # get the value of current year
        current_year = datetime.datetime.now().date().year

        # check if the crawler is first time used or continue work
        if not os.path.isdir(FIRE_DATA_DIR): # or change to path exist?
            os.makedirs(FIRE_DATA_DIR)

        # check all links
        all_fire_tuples, all_fire_links = self.crawler.extract_all_fires()

        # check for crawled fires from database
        crawled = set(self.dumper.retrieve_all_fires())

        # get the difference between all links and crawled
        to_crawl = set(all_fire_tuples).difference(crawled)

        # generate the final list of urls to crawl
        url_to_crawl = self.crawler.generate_url_from_tuple(to_crawl,current_year)

        # start to crawl
        for url in url_to_crawl:
            self.crawler.crawl(url)
            for folder in [f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]:
                absolute_path_folder = os.path.join(FIRE_DATA_DIR, folder)
                self.extractor.extract(absolute_path_folder, folder)








        if os.path.exists(FIRE_PROGRESS_DIR + "/crawler_history.txt"):
            with open(FIRE_PROGRESS_DIR + "/crawler_history.txt") as history:
                for line in history:
                    pair = line.strip().split(",")
                    self.explored_fire.add("{}{}/California/{}/".format(self.crawler.baseDir, pair[0], pair[1]))
        # self.explored: a set of explored links
        to_crawl = set(self.crawler.extract_all_fires()).difference(self.explored_fire)

        for link in to_crawl:
            self.crawler.crawl(link)


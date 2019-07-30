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




class DataFromFire(Runnable):
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
        all_fire_tuples = self.crawler.extract_all_fires()

        # check for crawled fires from database
        crawled = set(self.dumper.retrieve_all_fires())

        # get the difference between all links and crawled
        to_crawl = set(all_fire_tuples).difference(crawled)

        # generate the final list of urls to crawl
        url_to_crawl = self.crawler.generate_url_from_tuple(to_crawl,current_year)

        # start to crawl
        for url in url_to_crawl:
            self.crawler.crawl(url)
            # whether a record belongs to a sequence of fire is important
            # set up a bool value of this purpose
            if_sequence = False if len([f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]) == 1 else True
            for record in [f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]:
                # for a single fire, there can be multiple stages, which shows how this fire develops and dies out.
                # each stage should be treated as a separate record
                absolute_path_folder = os.path.join(FIRE_DATA_DIR, record)
                single_record = self.extractor.extract(absolute_path_folder, record, if_sequence)
                self.dumper.insert(single_record)
            self.crawler.cleanup()

        print("Fire information updated.")
        return








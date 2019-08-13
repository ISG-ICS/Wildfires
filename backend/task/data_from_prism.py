import logging
import time
from datetime import datetime, timedelta

import rootpath

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.crawler.prism_crawler import PRISMCrawler
from backend.data_preparation.extractor.bil_extractor import BILExtractor
from backend.data_preparation.dumper.prism_dumper import PRISMDumper

logger = logging.getLogger('TaskManager')


class DataFromPRISM(Runnable):
    def __init__(self):
        self.crawler = PRISMCrawler()
        self.crawler.set_extractor(BILExtractor())
        self.crawler.set_dumper(PRISMDumper())

    def run(self):
        self.crawler.start(datetime.now().date() - timedelta(days=7))


if __name__ == '__main__':
    while True:
        DataFromPRISM().run()
        time.sleep(3600 * 6)

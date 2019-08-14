import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import List

import rootpath

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.connection import Connection
from backend.data_preparation.crawler.prism_crawler import PRISMCrawler
from backend.data_preparation.extractor.bil_extractor import BILExtractor, BILFormat
from backend.data_preparation.dumper.prism_dumper import PRISMDumper

logger = logging.getLogger('TaskManager')


class DataFromPRISM(Runnable):
    def __init__(self):
        self.crawler = PRISMCrawler()
        self.extractor = BILExtractor()
        self.dumper = PRISMDumper()
        self.buffer: List[bytes] = list()

    def run(self, end_clause: datetime.date = None):
        current_date = datetime.now(timezone.utc).date()
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('select date, ppt, tmax, vpdmax from prism_info')
            exist_list = cur.fetchall()

            exist_dict = dict()
            for date, ppt, tmax, vpdmax in exist_list:
                exist_dict[date] = (ppt, tmax, vpdmax)

        date = current_date - timedelta(days=1)
        while date >= end_clause:

            logger.info(f'fetch: {date}')
            for var_idx, var in enumerate(PRISMCrawler.VARIABLES):
                # skip if exist
                if date in exist_dict and exist_dict[date][var_idx]:
                    logger.info(f'skip: {date}-{var}')
                    continue

                saved_filepath = self.crawler.crawl(date, var)
                if saved_filepath:
                    bil = self.extractor.extract(saved_filepath)  # type: BILFormat
                    if bil:
                        self.dumper.insert(date, bil.flattened, var)

                    # clean up
                    os.remove(saved_filepath)

            # finish crawling a day
            date = date - timedelta(days=1)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    while True:
        DataFromPRISM().run(datetime.now().date() - timedelta(days=7))
        time.sleep(3600 * 6)

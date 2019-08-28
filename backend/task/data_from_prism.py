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

    def run(self, end_clause: int = 7):
        """
        PRISM crawling routine

        :param end_clause: number of days we want to crawl. default = 7
        :return: None
        """
        current_date = datetime.now(timezone.utc).date()
        end_date = current_date - timedelta(days=end_clause)

        # get exist_list from DB
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('select date, ppt, tmax, vpdmax from prism_info')
            exist_list = cur.fetchall()

            exist_dict = dict()
            for date, ppt, tmax, vpdmax in exist_list:
                exist_dict[date] = (ppt, tmax, vpdmax)

        # crawl backward from today
        date = current_date - timedelta(days=1)
        while date >= end_date:

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
                        self.dumper.insert(date, bil.unflattened, var)

                    # clean up
                    os.remove(saved_filepath)

            # finish crawling a day
            date = date - timedelta(days=1)


if __name__ == '__main__':
    # these 2 lines enables logger output to stdout
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    while True:
        DataFromPRISM().run(2)
        logger.info('[PRISM][finished a round. Sleeping]')
        time.sleep(3600 * 6)

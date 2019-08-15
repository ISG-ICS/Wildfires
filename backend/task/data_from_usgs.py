import logging
import os
import time
from datetime import datetime, timedelta, timezone
from typing import List

import rootpath
from dateutil import parser as date_parser

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.crawler.usgs_crawler import USGSCrawler
from backend.data_preparation.extractor.usgs_extractor import BILExtractor
from backend.data_preparation.dumper.usgs_dumper import PRISMDumper

logger = logging.getLogger('TaskManager')


class DataFromUSGS(Runnable):
    def __init__(self):
        self.crawler = USGSCrawler()
        self.extractor = BILExtractor()
        self.dumper = PRISMDumper()
        self.buffer: List[bytes] = list()

    def run(self, end_clause: int = 7):
        """
        crawling routine
        :param end_clause: number of days we want to crawl, default=7
        :return: None
        """

        current_date = datetime.now(timezone.utc).date()
        end_date = current_date - timedelta(days=end_clause)

        # TODO: stop and continue
        # with Connection() as conn:
        #     cur = conn.cursor()
        #     cur.execute('select date, ppt, tmax, vpdmax from prism_info')
        #     exist_list = cur.fetchall()
        #
        #     exist_dict = dict()
        #     for date, ppt, tmax, vpdmax in exist_list:
        #         exist_dict[date] = (ppt, tmax, vpdmax)

        date = current_date - timedelta(days=7)  # website update weekly
        diff_date = date - date_parser.parse('20190730').date()
        date = date - timedelta(days=diff_date.days % 7)

        while date >= end_date:

            logger.info(f'[fetch]{date}')
            # skip if exist
            # if date in exist_dict and exist_dict[date][var_idx]:
            #     logger.info(f'skip: {date}-{var}')
            #     continue

            saved_filepath = self.crawler.crawl(date)
            if saved_filepath:
                # bil = self.extractor.extract(saved_filepath)  # type: BILFormat
                # if bil:
                #     self.dumper.insert(date, bil.flattened, var)

                # clean up
                os.remove(saved_filepath)

            # finish crawling a day
            date = date - timedelta(days=7)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    while True:
        DataFromUSGS().run(210)
        logger.info('[USGS][finished a round. Sleeping]')
        time.sleep(3600 * 6)

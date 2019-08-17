import logging
import os
import time
import zipfile
from datetime import datetime, timedelta, timezone
from typing import List

import rootpath
from dateutil import parser as date_parser

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.crawler.usgs_crawler import USGSCrawler
from backend.data_preparation.extractor.soil_mois_extractor import TiffExtractor
from backend.data_preparation.dumper.prism_dumper import PRISMDumper
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')


class DataFromUSGS(Runnable):
    def __init__(self):
        self.crawler = USGSCrawler()
        self.extractor = TiffExtractor()
        self.dumper = PRISMDumper()
        self.buffer: List[bytes] = list()

    def run(self, end_clause: int = 210):
        """
        crawling routine
        :param end_clause: number of days we want to crawl, default=7
        :return: None
        """

        current_date = datetime.now(timezone.utc).date()
        end_date = current_date - timedelta(days=end_clause)

        # TODO: stop and continue
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('select date from usgs_info')
            exist_list = cur.fetchall()
            cur.close()

        date = current_date - timedelta(days=7)  # website update weekly
        diff_date = date - date_parser.parse('20190730').date()
        date = date - timedelta(days=diff_date.days % 7)

        while date >= end_date:
            logger.info(f'[fetch]{date}')
            # skip if exist
            if (date,) in exist_list:
                logger.info(f'skip: {date}')

            saved_zip_path = self.crawler.crawl(date)
            if saved_zip_path is None:
                logger.info(f'{date} not found, skipped')

            else:
                zf = zipfile.ZipFile(saved_zip_path)
                for file in zf.namelist():
                    if file.split('.')[-4] == 'VI_NDVI' and file.split('.')[-1] == 'tif':
                        zf.extract(file, os.path.split(saved_zip_path)[0])
                        tif_file_name = file
                zf.close()
                tif_path = os.path.join(os.path.split(saved_zip_path)[0], tif_file_name)
                if tif_path is not None:
                    unflattened = self.extractor.extract(tif_path)
                    if unflattened is not None:
                        self.dumper.insert(date, unflattened, 'usgs')

                    # clean up
                    os.remove(saved_zip_path)
                    os.remove(tif_path)

            # finish crawling a day
            date = date - timedelta(days=7)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    while True:
        DataFromUSGS().run(end_clause=210)
        logger.info('[USGS][finished a round. Sleeping]')
        time.sleep(3600 * 6)

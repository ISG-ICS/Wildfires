import logging
import os
from datetime import datetime, date
from typing import Optional
from urllib import error

import rootpath
import wget

rootpath.append()
from backend.data_preparation.connection import Connection
from paths import SOIL_MOIS_DATA_DIR
from backend.data_preparation.crawler.crawlerbase import CrawlerBase

logger = logging.getLogger('TaskManager')


class SoilMoisCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.baseDir = 'https://nasagrace.unl.edu/GRACE/'
        self.select_exists = 'select datetime from env_soil_moisture group by datetime having count(*) = 810810'

    def start(self):
        pass

    def crawl(self, date_stamp: date) -> Optional[str]:
        formatted_date_stamp = date_stamp.strftime('%Y%m%d')
        file_url = self.baseDir + formatted_date_stamp + '/sfsm_perc_0125deg_US_' + formatted_date_stamp + '.tif'
        print(file_url)
        if not os.path.isdir(SOIL_MOIS_DATA_DIR):
            os.makedirs(SOIL_MOIS_DATA_DIR)
        try:
            wget.download(file_url, os.path.join(SOIL_MOIS_DATA_DIR, formatted_date_stamp + '.tif'))
        except error.HTTPError:
            logger.info('file: ' + formatted_date_stamp + ' not found, skipped')
        else:
            return os.path.join(SOIL_MOIS_DATA_DIR, formatted_date_stamp + '.tif')

    def get_exists(self) -> set:
        """get how far we went last time"""
        return set(Connection.sql_execute(self.select_exists))


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    crawler = SoilMoisCrawler()
    crawler.crawl(datetime.strptime("20131230", "%Y%m%d"))

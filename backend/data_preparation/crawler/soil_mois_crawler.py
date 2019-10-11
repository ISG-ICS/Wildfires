"""
@author: Tingxuan Gu
"""
import logging
import os
from datetime import datetime, date
from typing import Optional
from urllib import error

import rootpath
import wget

rootpath.append()
from backend.connection import Connection
from paths import SOIL_MOIS_DATA_DIR
from backend.data_preparation.crawler.crawlerbase import CrawlerBase

logger = logging.getLogger('TaskManager')


class SoilMoisCrawler(CrawlerBase):
    """
    This class is responsible for collecting data from NASAGrace
    """
    TIME_FORMAT = "%Y%m%d"

    def __init__(self):
        super().__init__()
        self.baseDir = 'https://nasagrace.unl.edu/GRACE'
        self.select_exists = 'select datetime from env_soil_moisture group by datetime having count(*) = 872505'

    def crawl(self, date_stamp: date) -> Optional[str]:
        """
        :param date_stamp: the date stamp of the file which is being crawled
        :return: crawled file's path if file exists on NASAGrace, else None
        """
        formatted_date_stamp = date_stamp.strftime('%Y%m%d')
        file_url = f'{self.baseDir}/{formatted_date_stamp}/sfsm_perc_0125deg_US_{formatted_date_stamp}.tif'
        if not os.path.isdir(SOIL_MOIS_DATA_DIR):
            os.makedirs(SOIL_MOIS_DATA_DIR)
        try:
            logger.info(f'trying to download file: {file_url}')
            wget.download(file_url, os.path.join(SOIL_MOIS_DATA_DIR, formatted_date_stamp + '.tif'))
        except error.HTTPError:
            logger.info(f'file: {file_url} not found, skipped')
        else:
            logger.info(f'file: {file_url} downloaded')
            return os.path.join(SOIL_MOIS_DATA_DIR, formatted_date_stamp + '.tif')

    def get_exists(self) -> set:
        """gets how far we went last time"""
        return set(Connection.sql_execute(self.select_exists))


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    target_date = "20131230"
    crawler = SoilMoisCrawler()
    crawler.crawl(datetime.strptime(target_date, SoilMoisCrawler.TIME_FORMAT))

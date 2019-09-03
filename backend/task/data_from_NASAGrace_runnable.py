"""
@author: Tingxuan Gu
"""
import glob
import logging
import os
from datetime import datetime, timedelta

from data_preparation.crawler.soil_mois_crawler import SoilMoisCrawler
from data_preparation.dumper.soil_mois_dumper import SoilMoisDumper
from data_preparation.extractor.soil_mois_extractor import TiffExtractor
from task.runnable import Runnable
from utilities.paths import SOIL_MOIS_DATA_DIR

logger = logging.getLogger('TaskManager')


class DataFromNASAGrace(Runnable):
    """
    This class is responsible for collecting data from NASAGrace
    """

    def __init__(self):
        self.crawler = SoilMoisCrawler()
        self.extractor = TiffExtractor()
        self.dumper = SoilMoisDumper()
        self.end_time = datetime.strptime('20160104', '%Y%m%d')

    def run(self, begin_time_str=datetime.today().strftime('%Y%m%d')) -> None:
        """
        The function that can be referenced in task manager
        Crawl, extract and dump data from NASAGrace
        :param begin_time_str: the earliest needed data's time
        :return: None
        """
        # get data from nasagrace
        begin_time = datetime.strptime(begin_time_str, '%Y%m%d')
        # make it a datetime object
        exists_set = self.crawler.get_exists()
        # crawl everyday's data from begin_time to end_time
        current_time = begin_time
        found_week_start = False
        while current_time > self.end_time:
            formatted_date_stamp = current_time.strftime('%Y%m%d')
            logger.info(f'start crawling for date {formatted_date_stamp}')

            try:
                if not found_week_start:
                    # to detect whether this is the last day with data
                    file_path = self.crawler.crawl(current_time) if (current_time,) not in exists_set else None
                    if file_path is not None:
                        self.extract_and_dump(file_path)
                        found_week_start = True
                    else:
                        current_time -= timedelta(days=1)
                else:
                    # start crawling every 7 days
                    current_time -= timedelta(days=7)
                    if (current_time,) not in exists_set:
                        file_path = self.crawler.crawl(current_time)
                        self.extract_and_dump(file_path)
                    else:
                        logger.info(f'{formatted_date_stamp} existed, skipped')
            finally:
                for tif_file in glob.glob(os.path.join(SOIL_MOIS_DATA_DIR, "*.tif")):
                    if 'res' not in tif_file and 'masked' not in tif_file:
                        os.remove(tif_file)
                    logger.info(f"file: {tif_file} removed")

        # if there are no files left, delete the directory
        for root, dirs, files in os.walk(SOIL_MOIS_DATA_DIR, topdown=False):
            if not files and not dirs:
                os.rmdir(root)
        logger.info(f'all data from {begin_time_str} to {self.end_time.strftime("%Y%m%d")}  processing finished')

    def extract_and_dump(self, file_path: str) -> None:
        """
        Using the file_path provided to extract the information needed and dump it into the database
        :param file_path: the data to be processed
        :return: None
        """
        data = self.extractor.extract(file_path)
        formatted_date_stamp = file_path.split('/')[-1].split('.')[0].split('/')[-1]
        logger.info(f'{formatted_date_stamp} extraction finished')
        self.dumper.insert(formatted_date_stamp, data)
        logger.info(f'{formatted_date_stamp} dumping finished')


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    DataFromNASAGrace().run()

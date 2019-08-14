import logging
import os
from datetime import datetime, timedelta

import rootpath

rootpath.append()
from backend.data_preparation.crawler.soil_mois_crawler import SoilMoisCrawler
from backend.data_preparation.dumper.soil_mois_dumper import SoilMoisDumper
from backend.data_preparation.extractor.soil_mois_extractor import SoilMoisExtractor
from backend.task.runnable import Runnable
from paths import SOIL_MOIS_DATA_DIR

logger = logging.getLogger('TaskManager')


class GetSoilMoisData(Runnable):
    def __init__(self):
        self.crawler = SoilMoisCrawler()
        self.extractor = SoilMoisExtractor()
        self.dumper = SoilMoisDumper()

    def run(self):
        # get data from nasagrace
        begin_time = (datetime.today() + timedelta(days=7)).strftime('%Y%m%d')  # remove the hours and minutes
        begin_time = datetime.strptime(begin_time, '%Y%m%d')  # put it back into a datetime object
        end_time = datetime.strptime('20131230', '%Y%m%d')  # make it a datetime object
        exists_list = self.crawler.get_exists()
        # crawl everyday's data from begin_time to end_time
        time_t = begin_time
        week_start_flag = False
        while time_t > end_time:
            formatted_date_stamp = time_t.strftime('%Y%m%d')
            logger.info('start crawling')
            if week_start_flag == False:
                # to detect whether this is the last day with data
                if (time_t,) not in exists_list:
                    test = self.crawler.crawl(time_t)
                if test is not None:
                    data = self.extractor.extract(os.path.join(SOIL_MOIS_DATA_DIR, formatted_date_stamp + '.tif'))
                    logger.info('extraction finished')
                    self.dumper.insert(test, data)
                    logger.info('dumping finished')
                    week_start_flag = True
                else:
                    time_t -= timedelta(days=1)
            # start crawling every 7 days
            if week_start_flag == True:
                time_t -= timedelta(days=7)
                if (time_t,) not in exists_list:
                    stamp = self.crawler.crawl(time_t)
                    data = self.extractor.extract(os.path.join(SOIL_MOIS_DATA_DIR, formatted_date_stamp + '.tif'))
                    logger.info('extraction finished')

                    self.dumper.insert(stamp, data)
                    logger.info('dumping finished')

        # if there are no files left, delete the directory
        for root, dirs, files in os.walk(SOIL_MOIS_DATA_DIR, topdown=False):
            if not files and not dirs:
                os.rmdir(root)
        logger.info('all data processing finished')


if __name__ == '__main__':
    GetSoilMoisData().run()

import logging
import os
import traceback
from datetime import datetime, timedelta

import requests
import rootpath

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
        # get data from nasagrace
        begin_time = (datetime.today() + timedelta(days=7)).strftime('%Y%m%d')  # remove the hours and minutes
        begin_time = datetime.strptime(begin_time, '%Y%m%d')  # put it back into a datetime object
        end_time = datetime.strptime('20131230', '%Y%m%d')  # make it a datetime object
        exists_list = self.get_exists()
        # crawl everyday's data from begin_time to end_time
        time_t = begin_time
        week_start_flag = False
        while time_t > end_time:
            if week_start_flag == False:
                # to detect whether this is the last day with data
                if (time_t,) not in exists_list:
                    test = self.crawl(time_t)
                if test is not None:
                    week_start_flag = True
                else:
                    time_t -= timedelta(days=1)
            if week_start_flag == True:
                time_t -= timedelta(days=7)
                if (time_t,) not in exists_list:
                    self.crawl(time_t)

    def crawl(self, date_stamp):
        formatted_date_stamp = date_stamp.strftime('%Y%m%d')
        file_url = self.baseDir + formatted_date_stamp + '/sfsm_perc_0125deg_US_' + formatted_date_stamp + '.tif'
        try:
            response = requests.get(url=file_url)
            if response.status_code != 200:
                logger.error('file: ' + formatted_date_stamp + ' not found')
                return None
            else:
                # create dirs
                if not os.path.isdir(SOIL_MOIS_DATA_DIR):
                    os.makedirs(SOIL_MOIS_DATA_DIR)
                # write file
                with open(os.path.join(SOIL_MOIS_DATA_DIR, formatted_date_stamp + '.tif'), 'wb') as f:
                    f.write(response.content)
                    logger.info('saved file: ' + formatted_date_stamp)
        except IOError:
            logger.error('error: ' + traceback.format_exc())
        return date_stamp.strftime('%Y-%m-%d')

    def get_exists(self):
        """get how far we went last time"""
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute(self.select_exists)
            exists_list = cur.fetchall()
            cur.close()
        return exists_list


if __name__ == '__main__':
    while True:
        crawler = SoilMoisCrawler()
        crawler.start()

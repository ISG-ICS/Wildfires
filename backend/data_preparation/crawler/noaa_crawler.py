import logging
import math
import os
import sys
import time
import traceback
from datetime import datetime, timedelta, timezone

import requests
import rootpath

from backend.data_preparation.dumper.dumperbase import DumperException

rootpath.append()

from paths import GRIB2_DATA_DIR
from backend.data_preparation.connection import Connection
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.dumper.noaa_dumper import NOAADumper

logger = logging.getLogger('TaskManager')


class NOAACrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.baseDir = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl'
        self.useJavaConverter = False  # use grib2json?
        self.interval = 6
        self.select_exists = 'select reftime from noaa0p25_reftime'

    def start(self, end_clause=None):
        # verify if both extractor and dumper are set up, raise ExtractorException or DumperException respectively
        if not self.dumper:
            raise DumperException

        exists_list = self.get_exists()

        # get data from noaa.gov
        current_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-7))).replace(tzinfo=None)  # PDT
        begin_time = current_time + timedelta(hours=self.interval)
        end_time = current_time - timedelta(hours=240)  # specify the oldest data we can get.

        # round datetime to 6 hours
        time_t = begin_time - timedelta(hours=begin_time.hour - int(self.round_to_hour(begin_time.hour, self.interval)),
                                        minutes=begin_time.minute,
                                        seconds=begin_time.second,
                                        microseconds=begin_time.microsecond)
        while time_t >= end_time:
            if (time_t,) not in exists_list:
                self.crawl(time_t)
            time_t -= timedelta(hours=self.interval)

    def crawl(self, t):
        clock = t.timetuple()
        date = t.strftime('%Y%m%d')
        hour = self.round_to_hour(clock.tm_hour, self.interval)
        stamp = date + hour
        stamp2 = date + '/' + hour

        # parameters of GET
        qs = {
            'file': 'gfs.t' + hour + 'z.pgrb2.0p25.f000',
            'lev_100_m_above_ground': 'on',
            'lev_0-0.1_m_below_ground': 'on',
            'var_UGRD': 'on',
            'var_VGRD': 'on',
            'var_TMP': 'on',
            'var_SOILW': 'on',
            'leftlon': 0,
            'rightlon': 360,
            'toplat': 90,
            'bottomlat': -90,
            'dir': '/gfs.' + stamp2
        }
        try:
            response = requests.get(url=self.baseDir, params=qs)
            if response.status_code != 200:
                # try -6h
                logger.error('file: ' + stamp + ' not found')
            else:
                # create dirs
                if not os.path.isdir(GRIB2_DATA_DIR):
                    os.makedirs(GRIB2_DATA_DIR)
                # write file
                with open(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'), 'wb') as f:
                    f.write(response.content)
                    logger.info('saved file: ' + stamp)
        except IOError:
            # try -6h
            logger.error('error: ' + traceback.format_exc())
        return stamp

    def get_exists(self):
        """get how far we went last time"""
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute(self.select_exists)
            exists_list = cur.fetchall()
            cur.close()
        return exists_list

    @staticmethod
    def round_to_hour(hour, interval) -> str:
        if interval > 0:
            result = math.floor(hour / interval) * interval
            return str(result) if result >= 10 else '0' + str(result)
        else:
            raise RuntimeError('interval should NOT set to zero')
            logger.error('error: interval should NOT set to zero')

    @staticmethod
    def remove_grib2_file(stamp):
        # clear cached grib2 data after finish
        if os.path.isfile(os.path.join(GRIB2_DATA_DIR, stamp + '.f000')):
            os.remove(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'))


if __name__ == '__main__':
    while True:
        crawler = NOAACrawler()
        crawler.set_dumper(NOAADumper())
        for arg in sys.argv:
            if arg == '-j':
                crawler.useJavaConverter = True  # use java version of grib2json, if '-j' appeared
        crawler.start()

        print('\tWaiting for 6 hours')
        time.sleep(3600 * 6)

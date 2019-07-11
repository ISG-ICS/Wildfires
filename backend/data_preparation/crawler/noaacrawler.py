import os
import sys
import time
from datetime import datetime, timedelta

import math
import requests
import rootpath

rootpath.append()

from configurations import GRIB2_DATA_DIR
from backend.data_preparation.connection import Connection
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.extractor.gribextractor import GRIBExtractor
from backend.data_preparation.dumper.noaadumper import NOAADumper


class NOAACrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.baseDir = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl'
        self.useJavaConverter = False  # use grib2json?
        self.interval = 6
        self.select_exists = 'select reftime from noaa0p25_reftime'

    def start(self, end_clause=None):
        # get how far we went last time
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute(self.select_exists)
            exists_list = cur.fetchall()
            cur.close()

        # get data from noaa.gov
        currentTime = datetime.today()
        beginTime = currentTime + timedelta(hours=self.interval)
        endTime = currentTime - timedelta(hours=12)  # specify the oldest data we can get.

        # round datetime to 6 hours
        time_t = beginTime - timedelta(hours=beginTime.hour - int(self.roundHour(beginTime.hour, self.interval)),
                                       minutes=beginTime.minute,
                                       seconds=beginTime.second,
                                       microseconds=beginTime.microsecond)
        while time_t >= endTime:
            if (time_t,) not in exists_list:
                self.runQuery(time_t)
            time_t -= timedelta(hours=self.interval)

    def crawl(self, *args, **kwargs) -> list:
        return list()

    def runQuery(self, t):
        time = t.timetuple()
        date = t.strftime('%Y%m%d')
        hour = self.roundHour(time.tm_hour, self.interval)
        stamp = date + hour
        stamp2 = date + '/' + hour

        # parameters of GET
        qs = {
            'file': 'gfs.t' + hour + 'z.pgrb2.0p25.anl',
            'lev_100_m_above_ground': 'on',  # all vars are present on this level
            'var_UGRD': 'on',
            'var_VGRD': 'on',
            'var_TMP': 'on',
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
                print(stamp + ' not found')
            else:
                # create dirs
                if not os.path.isdir(GRIB2_DATA_DIR):
                    os.makedirs(GRIB2_DATA_DIR)
                # write file
                with open(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'), 'wb') as f:
                    f.write(response.content)
                    print('saved')
                # convert format
                ext_ugnd = GRIBExtractor(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'), 'U component of wind', None)
                ext_vgnd = GRIBExtractor(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'), 'V component of wind', None)
                ext_tmp = GRIBExtractor(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'), 'Temperature', None)
                print('converted')

                # dump into DB
                self.set_dumper(NOAADumper())
                self.dumper.insert(ext_ugnd.data, ext_vgnd.data, ext_tmp.data, t, stamp)
        except IOError as e:
            # try -6h
            print(e)
        finally:
            # clear cached grib2 data after finish
            if os.path.isfile(os.path.join(GRIB2_DATA_DIR, stamp + '.f000')):
                os.remove(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'))

    @staticmethod
    def roundHour(hour, interval) -> str:
        if interval > 0:
            result = (math.floor(hour / interval) * interval)
            return str(result) if result >= 10 else '0' + str(result)
        else:
            raise RuntimeError('interval should NOT set to zero')


if __name__ == '__main__':
    while True:
        crawler = NOAACrawler()
        for arg in sys.argv:
            if arg == '-j':
                crawler.useJavaConverter = True  # use java version of grib2json, if '-j' appeared
        crawler.start()

        print('\tWaiting for 6 hours')
        time.sleep(3600 * 6)

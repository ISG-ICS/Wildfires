import requests
from datetime import datetime, timedelta
import math
import os
import sys
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.extractor.WindExtractor import WindExtractor
from configurations import GRIB2_DATA_DIR


class WindCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()
        self.baseDir = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl'
        self.useJavaConverter = False  # use grib2json?
        self.interval = 6

    def start(self, end_clause=None):
        # get the latest wind data from noaa.gov
        currentTime = datetime.today()
        self.runQuery(currentTime + timedelta(hours=self.interval))

    def __getitem__(self, index):
        pass

    def runQuery(self, t):
        time = t.timetuple()
        date = t.strftime('%Y%m%d')
        hour = self.roundHour(time.tm_hour, self.interval)
        stamp = date + hour
        stamp2 = date + '/' + hour

        # parameters of GET
        qs = {
            'file': 'gfs.t' + hour + 'z.pgrb2.0p25.anl',
            'lev_20_m_above_ground': 'on',
            'var_UGRD': 'on',
            'var_VGRD': 'on',
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
                self.runQuery(t - timedelta(hours=self.interval))
            else:
                # create dirs
                if not os.path.isdir(GRIB2_DATA_DIR):
                    os.makedirs(GRIB2_DATA_DIR)
                # write file
                with open(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'), 'wb') as f:
                    f.write(response.content)
                print('saved')

                # convert format
                self.inject_extractor(WindExtractor(os.path.join('grib-data', stamp + '.f000'), None, None))
                self.extractor.extract(stamp, self.useJavaConverter)
        except IOError as e:
            # try -6h
            print(e)
            self.runQuery(t - timedelta(hours=self.interval))
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
    crawler = WindCrawler()
    for arg in sys.argv:
        if arg == '-j':
            crawler.useJavaConverter = True  # use java version of grib2json, if '-j' appeared

    crawler.start()
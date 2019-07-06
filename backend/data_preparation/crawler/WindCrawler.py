import requests
from datetime import datetime, timedelta
import math
import os
import sys
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.extractor.WindExtractor import WindExtractor

baseDir = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl'
useJavaConverter = False  # use grib2json?


class WindCrawler(CrawlerBase):
    def __init__(self):
        super().__init__()

    def start(self, end_clause=None, *args, **kwargs):
        # get the latest wind data from noaa.gov
        t = datetime.today()
        self.runQuery(t + timedelta(hours=6))

    def __getitem__(self, index):
        pass

    def runQuery(self, t):
        time = t.timetuple()
        date = t.strftime('%Y%m%d')
        hour = self.roundHour(time.tm_hour, 6)
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
            r = requests.get(url=baseDir, params=qs)
            if r.status_code != 200:
                # try -6h
                print(stamp + ' not found')
                self.runQuery(t - timedelta(hours=6))
            else:
                # create dirs
                if not os.path.isdir('grib-data'):
                    os.makedirs('grib-data')
                # write file
                with open(os.path.join('grib-data', stamp + '.f000'), 'wb') as f:
                    f.write(r.content)
                print('saved')

                # convert format
                self.inject_extractor(WindExtractor(os.path.join('grib-data', stamp + '.f000'), None, None))
                self.extractor.extract(stamp, useJavaConverter)
        except IOError as e:
            # try -6h
            print(e)
            self.runQuery(t - timedelta(hours=6))

    @staticmethod
    def roundHour(hour, interval) -> str:
        if interval > 0:
            result = (math.floor(hour / interval) * interval)
            return str(result) if result >= 10 else '0' + str(result)


def main():
    for arg in sys.argv:
        if arg == '-j':
            global useJavaConverter
            useJavaConverter = True
    crawler = WindCrawler()
    crawler.start()


if __name__ == '__main__':
    main()

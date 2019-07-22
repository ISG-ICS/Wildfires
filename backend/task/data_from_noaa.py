import os
import sys
import time
from datetime import datetime, timedelta, timezone

import rootpath

from paths import GRIB2_DATA_DIR

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.crawler.noaa_crawler import NOAACrawler
from backend.data_preparation.extractor.grib_extractor import GRIBExtractor, GRIBEnum
from backend.data_preparation.dumper.noaa_dumper import NOAADumper


class DataFromNoaa(Runnable):
    def __init__(self):
        self.crawler = NOAACrawler()
        self.dumper = NOAADumper()

    def run(self):
        for arg in sys.argv:
            if arg == '-j':
                self.crawler.useJavaConverter = True  # use java version of grib2json, if '-j' appeared
        exists_list = self.crawler.get_exists()

        # get data from noaa.gov
        current_time = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=-7))).replace(tzinfo=None)  # PDT
        begin_time = current_time + timedelta(hours=self.crawler.interval)
        end_time = current_time - timedelta(hours=240)  # specify the oldest data we can get.

        # round datetime to 6 hours
        time_t = begin_time - timedelta(
            hours=begin_time.hour - int(self.crawler.round_to_hour(begin_time.hour, self.crawler.interval)),
            minutes=begin_time.minute,
            seconds=begin_time.second,
            microseconds=begin_time.microsecond)
        while time_t >= end_time:
            if (time_t,) not in exists_list:
                # crawl the data from website
                stamp = self.crawler.crawl(time_t)

                # extract data from files
                extractor = GRIBExtractor(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'))
                ugnd = extractor.extract(GRIBEnum.NOAA_WIND_U)
                vgnd = extractor.extract(GRIBEnum.NOAA_WIND_V)
                tmp = extractor.extract(GRIBEnum.NOAA_TMP)
                soilw = extractor.extract(GRIBEnum.NOAA_SOILW)
                print('extracted')

                # dump the extracted data into database
                self.dumper.insert(ugnd, vgnd, tmp, soilw, time_t, stamp)
                print('dumped')

                # remove the dumped data file
                self.crawler.remove_grib2_file(stamp)

            time_t -= timedelta(hours=self.crawler.interval)
        print('time to sleep')


if __name__ == '__main__':
    while True:
        DataFromNoaa().run()
        time.sleep(3600 * 6)

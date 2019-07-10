#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import os
from urllib.request import urlopen
import wget

import requests
from bs4 import BeautifulSoup
from flask import Response
import rootpath

rootpath.append()

from configurations import REC_TEMP_MOIS_PATH, HIS_MOIS_PATH, HIS_TEMP_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.dumper.mois_temp_dumper import MoisTempDumper
from backend.data_preparation.extractor.gribextractor import GRIBExtractor
from backend.data_preparation.extractor.tifextractor import TIFExtractor
from backend.data_preparation.extractor.url_classifier import timeout, TimeoutException
from backend.data_preparation.connection import Connection


class MoisTempCrawler(CrawlerBase):
    HIS_TEMP_MODE = 0
    HIS_MOIS_MODE = 1
    REC_TEMP_MODE = 2
    REC_MOIS_MODE = 3

    ERROR_LOG = '/error_urls.txt'
    ERROR_LOG_NEW = '/error_urls_new.txt'

    HIS_TEMP_BASE_URL = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/'
    HIS_MOIS_BASE_URL = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/'
    REC_TEMP_MOIS_BASE_URL = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.'

    MOIS_PROP_NAME = 'Liquid volumetric soil moisture (non-frozen)'
    TEMP_PROP_NAME = 'temperature'
    TEMP_PROP_TYPEOFLEVEL = 'surface'

    def __getitem__(self, index):
        # get item from in-memory structure self.data
        return self.data

    def start(self, end_clause=None, data_type=None, run_count=0):

        # set up connection to databse
        conn = Connection()()

        # set up dumper
        dumper = MoisTempDumper()
        self.set_dumper(dumper)

        if data_type == MoisTempCrawler.HIS_TEMP_MODE:

            # call crawler to crawl information to files
            self.run_historical_crawler(HIS_TEMP_PATH, MoisTempCrawler.HIS_TEMP_BASE_URL)

            # call dumper for historical temp & mois
            self.data_process(conn, HIS_TEMP_PATH, data_type)

        elif data_type == MoisTempCrawler.HIS_MOIS_MODE:

            # call crawler to crawl information to files
            self.run_historical_crawler(HIS_MOIS_PATH, MoisTempCrawler.HIS_MOIS_BASE_URL)

            # call dumper for historical temp & mois
            self.data_process(conn, HIS_MOIS_PATH, data_type)

        elif data_type == MoisTempCrawler.REC_TEMP_MODE or data_type == MoisTempCrawler.REC_MOIS_MODE:

            # call crawler to crawl information to files
            self.run_recent_crawler(REC_TEMP_MOIS_PATH, MoisTempCrawler.REC_TEMP_MOIS_BASE_URL, run_count)

            # call dumper for recent temp & mois
            self.data_process(conn, REC_TEMP_MOIS_PATH, data_type, run_count)

    def crawl(self, path_to_save_data: str, url_to_get_data: str):
        if not os.path.exists(path_to_save_data):
            os.makedirs(path_to_save_data)
        datafile_list = self.get_datafile_list_from_url(url_to_get_data)

        for single_datafile in datafile_list:
            datafile_name = single_datafile.get('href')
            if self.filename_fit_requirements(datafile_name):
                full_datafile_url = url_to_get_data + datafile_name
                print(full_datafile_url)

                try:
                    returned_req = self.get_request(full_datafile_url)
                except TimeoutException or returned_req is None:
                    path_to_error_log = path_to_save_data + MoisTempCrawler.ERROR_LOG
                    self.write_error_url_to_log(full_datafile_url, path_to_error_log)
                    continue

                self.download_file_from_url(datafile_name, url_to_get_data, path_to_save_data)

        while os.path.exists(path_to_error_log):  # there exists error urls
            for error_url in open(path_to_error_log):
                try:
                    returned_req = self.get_request(error_url)
                except TimeoutException or returned_req is None:
                    path_to_new_error_log = path_to_save_data + MoisTempCrawler.ERROR_LOG_NEW
                    self.write_error_url_to_log(error_url, path_to_new_error_log)
                    continue

                file_name = error_url.split('/')[-1]
                if 'historical' in path_to_save_data:  # write historical data into files
                    # error tif file sample: http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/t.full.20190519.tif
                    full_path_to_save_file = path_to_save_data + '/' + file_name

                elif 'recent' in path_to_save_data:  # write recent data into files
                    # error_url sample: https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.20190711/cdas1.t00z.sfluxgrbf00.grib2
                    file_date = error_url.split('/')[-2].split('.')[-1]
                    full_path_to_save_file = path_to_save_data + '/' + file_name + '_' + file_date + '.txt'

                wget.download(error_url, full_path_to_save_file)

            self.update_error_urls_file(path_to_save_data)

    def get_datafile_list_from_url(self, url):
        html = urlopen(url)
        bs_obj = BeautifulSoup(html, 'html.parser')
        datafile_list = bs_obj.find_all('a')
        return datafile_list

    def filename_fit_requirements(self, file_name: str) -> bool:
        """return true of false to decide whether this file is needed to be crawled
            recent data file_name sample: cdas1.t00z.sfluxgrbf00.grib2
            historical data file name sample: w.full.20190519.tif
        """
        # to get the second '00' and we only want the '00'~'06' file
        if ('sfluxgrbf' in file_name and 'idx' not in file_name and int(file_name.split('.')[-2][-2:-1]) <= 6) \
                or ('tif' in file_name):
            return True
        else:
            return False

    def download_file_from_url(self, datafile_name, url_to_get_data, path_to_save_data):
        # sample datafile_name: cdas1.t00z.sfluxgrbf00.grib2
        if 'sfluxgrbf' in datafile_name:
            # url_to_get_data sample: https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.20190711/
            file_date = url_to_get_data.split('/')[-2].split('.')[-1]
            full_path_to_save_file = path_to_save_data + '/' + datafile_name + '_' + file_date + '.txt'

        # sample datafile_name: w.full.20190519.tif
        elif 'tif' in datafile_name:
            full_path_to_save_file = path_to_save_data + '/' + datafile_name

        wget.download(url_to_get_data, full_path_to_save_file)

    @staticmethod
    @timeout(20)
    def get_request(file_url: str) -> Response:
        """return a file with provided url, if the request got timeout, a TimeoutException will be raised
        :file_url str supplied full url
        :returns flask.Response
        :raises backend.data_preparation.extractor.url_classifier.TimeoutException
        """
        return requests.get(file_url)

    def write_error_url_to_log(self, error_url, path_to_error_log):
        with open(path_to_error_log, 'a') as error_file:
            error_file.append(error_url + '\n')

    def update_error_urls_file(self, path_to_error_urls):
        os.remove(path_to_error_urls + MoisTempCrawler.ERROR_LOG)  # get rid of the older error url file
        if os.path.exists(
                path_to_error_urls + MoisTempCrawler.ERROR_LOG_NEW):  # change the new error url file's name into the older one
            os.rename(path_to_error_urls + MoisTempCrawler.ERROR_LOG_NEW,
                      path_to_error_urls + MoisTempCrawler.ERROR_LOG)

    def run_historical_crawler(self, path, url):
        # start crawling information to files
        # and run until there aren't any undealed error urls
        self.crawl(path, url)
        print(url)
        while os.path.exists(path + MoisTempCrawler.ERROR_LOG):
            self.recall_crawl(path)

    def run_recent_crawler(self, path, url, run_count=1):
        # start crawling information to files
        # and run until there aren't any undealed error urls
        for cur_run_count in range(1, run_count + 1):
            date = self.get_date(cur_run_count)
            self.crawl(path, url + date + '/')
            while os.path.exists(path + MoisTempCrawler.ERROR_LOG):
                self.recall_crawl(path)

    def data_process(self, conn, path, data_type, run_count=1):
        # run extractor and dumper

        # all files in path
        files = os.listdir(path)

        if data_type == MoisTempCrawler.HIS_TEMP_MODE or data_type == MoisTempCrawler.HIS_MOIS_MODE:

            # extract data from each ".tif" file and dump to database
            for file in files:
                if not os.path.isdir(file) and 'tif' in file:

                    # call extractor to get dictionary from file
                    tif_extractor = self.run_tif_extractor(path, file)

                    # dump each (key, value) from extractor's dictionary
                    for key, value in tif_extractor.data.items():

                        lat, long, time = self.historical_value_expand(key)

                        # dump temp or mois data if not equals to '-999000000'
                        if str(value) != '-999000000':
                            # call dumper to dump into database
                            self.run_dumper(data_type, conn, p_lat=lat, p_long=long, p_value=float(value),
                                            p_time=time)

                # remove all dumped files
                os.remove(path + '/' + file)

        elif data_type == MoisTempCrawler.REC_TEMP_MODE or data_type == MoisTempCrawler.REC_MOIS_MODE:
            # traverse recent days according to parameter run_count
            for count in range(1, run_count + 1):

                # get corresponding date
                date = self.get_date(count)

                # extract data from each ".grib" file and dump to database
                for file in files:
                    if not os.path.isdir(file) and 'txt' in file and date in file:

                        file = path + '/' + file

                        # call extractor to get dictionary from file
                        grib_extractor = self.run_grib_extractor(data_type, file)

                        # get start time and end time for one record
                        start_time, end_time = self.get_start_end_time(file, date)

                        # dump each (key, value) from extractor's dictionary
                        for key, value in grib_extractor.data.items():

                            lat, long, value = self.recent_value_expand(key, value)

                            # dump temp or mois data if not equals to 'nan'
                            if str(value) != 'nan':
                                self.run_dumper(data_type, conn, p_lat=lat, p_long=long, p_value=value,
                                                p_start=start_time, p_end=end_time)

                        # remove all dumped files
                        os.remove(path + '/' + file)

    def historical_value_expand(self, key):
        # format key into lat, long, time
        lat = float(key[0])
        long = 360 + float(key[1])
        time = key[2]
        return lat, long, time

    def recent_value_expand(self, key, value):
        # format (key, value) into lat, long, value
        lat = float(key[1:key.find(',')])
        long = float(key[key.find(',') + 1:key.find(')')])
        v = float(value)
        return lat, long, v

    def run_tif_extractor(self, path, file):
        # call TIF Extractor
        tif_extractor = TIFExtractor(path + '/' + file)
        tif_extractor.extract()
        return tif_extractor

    def run_grib_extractor(self, data_type, file):
        # call GRIB Extractor
        grib_extractor = GRIBExtractor(file)
        grib_extractor.extract(data_type)
        return grib_extractor

    def run_dumper(self, data_type, conn, p_lat, p_long, p_value,
                   p_time=0, p_start=0, p_end=0):
        info = {"data_type": data_type, "conn": conn, "p_lat": p_lat, "p_long": p_long,
                "p_value": p_value, "p_time": p_time, "p_start": p_start, "p_end": p_end}
        self.dumper.insert(info)

    def get_start_end_time(self, file, date):
        # get start time and end time according to file name and date
        start_hour = int(file[file.find('.t') + 2:file.find('z')])
        end_hour = start_hour + int(file[file.find('grbf') + 4:file.find('.grib2')])
        start_time = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), start_hour, 0, 0)
        end_time = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), end_hour, 0, 0)
        return start_time, end_time

    def get_date(self, count):
        # get date from today according to the parameter count
        curDate = datetime.datetime.today() - datetime.timedelta(days=count)
        formattedDate = curDate.strftime('%y%m%d')
        date = '20' + str(formattedDate)
        return date


if __name__ == '__main__':
    crawler = MoisTempCrawler()

    # crawl all the historical temperature data, extract and dump into database
    crawler.start(data_type=MoisTempCrawler.HIS_TEMP_MODE)

    # crawl all the historical moisture data, extract and dump into database
    crawler.start(data_type=MoisTempCrawler.HIS_MOIS_MODE)

    # crawl recent temperature data, extract and dump into database
    # run_count = 1 for yesterday data, 6 for recent 6 days data (for the first time execution, run_count = 6)
    crawler.start(data_type=MoisTempCrawler.REC_TEMP_MODE, run_count=1)

    # crawl recent moisture data, extract and dump into database
    # run_count = 1 for yesterday data, 6 for recent 6 days data (for the first time execution, run_count = 6)
    crawler.start(data_type=MoisTempCrawler.REC_MOIS_MODE, run_count=1)

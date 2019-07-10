#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup
import datetime
import psycopg2
import rootpath
rootpath.append()
from configurations import REC_TEMP_MOIS_PATH, HIS_MOIS_PATH, HIS_TEMP_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from mois_temp_dumper import MoistureTemperatureDumper
from gribextractor import GRIBExtractor
from tifextractor import TIFExtractor


class MoisTempCrawler(CrawlerBase):

    HIS_TEMP_MODE = 0
    HIS_MOIS_MODE = 1
    REC_TEMP_MODE = 2
    REC_MOIS_MODE = 3

    ERROR_LOG = '/error_urls.txt'

    HIS_TEMP_URL = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/'
    HIS_MOIS_URL = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/'
    REC_TEMP_MOIS_URL = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.'

    MOIS_PROP_NAME = 'Liquid volumetric soil moisture (non-frozen)'
    TEMP_PROP_NAME = 'temperature'
    TEMP_PROP_TYPEOFLEVEL = 'surface'


    def __getitem__(self, index):
        # get item from in-memory structure self.data
        pass

    def start(self, end_clause=None, data_type=None, run_count = 0):

        # set up connection to databse
        conn = psycopg2.connect(dbname="testdb", user="tester", password="testpassword",
                                host="cloudberry05.ics.uci.edu", port="5432")

        # set up dumper
        dumper = MoistureTemperatureDumper()
        self.inject_dumper(dumper)

        if data_type == MoisTempCrawler.HIS_TEMP_MODE:

            # call crawler to crawl information to files
            self.call_crawler(HIS_TEMP_PATH, MoisTempCrawler.HIS_TEMP_URL)

            # call dumper for historical temp & mois
            self.call_his_dumper(conn, HIS_TEMP_PATH, data_type)

        elif data_type == MoisTempCrawler.HIS_MOIS_MODE:

            # call crawler to crawl information to files
            self.call_crawler(HIS_MOIS_PATH, MoisTempCrawler.HIS_MOIS_URL)

            # call dumper for historical temp & mois
            self.call_his_dumper(conn, HIS_MOIS_PATH, data_type)

        elif data_type == MoisTempCrawler.REC_TEMP_MODE or data_type == MoisTempCrawler.REC_MOIS_MODE:

            # call crawler to crawl information to files
            self.call_crawler(REC_TEMP_MOIS_PATH, MoisTempCrawler.REC_TEMP_MOIS_URL)

            # call dumper for recent temp & mois
            self.call_rec_dumper(conn, REC_TEMP_MOIS_PATH, data_type, run_count)



    def crawl(self, path, url):
        if not os.path.exists(path):
            os.makedirs(path)
        file_list = self.get_filelist_from_url(url)

        for web_file in file_list:
            file_name = web_file.get('href')
            if ('sfluxgrbf' in file_name and 'idx' not in file_name
                and int(file_name[file_name.find('grbf') + 4: file_name.find('.grib2')]) <= 6) \
                    or ('tif' in file_name):  # to determine which kind of files to grab
                file_url = url + file_name
                print(file_url)

                # if the url request got stuck, return None, save this url to the file saving error urls
                # continue to next url
                # if not stuck, return the url request's content
                req = self.timeout_handling(file_url, path + '/error_urls.txt')
                if req.eq(None):
                    continue

                if 'sfluxgrbf' in file_name:  # indicate it's a recent data file
                    file_date = url[url.find('cdas.') + 5: url.find('cdas.') + 13]  # collect date from url
                    file_path = path + '/' + file_name + '_' + file_date + '.txt'
                    self.write_request_file(file_path, req.content)

                if 'tif' in file_name:  # indicate it's a historical data file
                    file_path = path + '/' + file_name
                    self.write_request_file(file_path, req.content)

    def recall_crawl(self, path):
        # recall the error urls in the file and re-download them
        if not os.path.exists(path):
            os.makedirs(path)

        if os.path.exists(path + '/error_urls.txt'):  # there exists error urls
            for url in open(path + '/error_urls.txt'):
                req = self.timeout_handling(url.strip('\n'), path + '/error_urls_new.txt')
                if req.eq(None):
                    continue

                if 'historical' in path and 'temp' in url:  # write historical temperature data into files
                    file_name = url[url.find('t.full'):url.find('.tif') + 4]
                    file_path = path + '/' + file_name
                    self.write_request_file(file_path, req.content)

                if 'historical' in path and 'soil' in url:  # write historical moisture data into files
                    file_name = url[url.find('w.full'):url.find('.tif') + 4]
                    file_path = path + '/' + file_name
                    self.write_request_file(file_path, req.content)

                if 'recent' in path:  # write recent data into files
                    file_date = url[url.find('cdas.') + 5: url.find('cdas.') + 13]
                    file_name = url[url.find('cdas1.'):url.find('.grib2') + 6]
                    file_path = path + '/' + file_name + '_' + file_date + '.txt'
                    self.write_request_file(file_path, req.content)

            self.update_error_urls_file(path)


    def get_filelist_from_url(self, url):
        html = urlopen(url)
        bs_obj = BeautifulSoup(html, 'html.parser')
        file_list = bs_obj.find_all('a')
        return file_list

    def timeout_handling(self, file_url, path_to_error_urls):
        start_time = time.process_time()
        req = requests.get(file_url)
        end_time = time.process_time()

        if end_time - start_time > 20:
            with open(path_to_error_urls, 'a') as error_file:
                error_file.write(file_url + '\n')
            return None
        else:
            return req.content

    def write_request_file(self, file_path, content):
        with open(file_path, 'wb') as file_to_write:
            file_to_write.write(content)

    def update_error_urls_file(self, path_to_error_urls):
        os.remove(path_to_error_urls + '/error_urls.txt')  # get rid of the older error url file
        if os.path.exists(
                path_to_error_urls + '/error_urls_new.txt'):  # change the new error url file's name into the older one
            os.rename(path_to_error_urls + '/error_urls_new.txt', path_to_error_urls + '/error_urls.txt')


    def call_crawler(self, path, url):
        # start crawling information to files
        # and run until there aren't any undealed error urls
        while os.path.exists(path + MoisTempCrawler.ERROR_LOG):
            self.crawl(path, url)
            self.recall_crawl(path)

    def call_his_dumper(self, conn, path, data_type):
        # all files in path
        files = os.listdir(path)

        # extract data from each ".tif" file and dump to database
        for file in files:
            if not os.path.isdir(file) and 'tif' in file:

                # call extractor to get dictionary from file
                tif_extractor = self.call_tif_extractor(path, file)

                # dump each (key, value) from extractor's dictionary
                for key, value in tif_extractor.data.items():

                    lat, long, time = self.his_value_expand(key)

                    # dump temp or mois data if not equals to '-999000000'
                    if str(value) != '-999000000':
                        # call dumper to dump into database
                        self.dumper.insert_one(conn, data_type, p_lat=lat, p_long=long, p_value=float(value), p_time=time)

                # remove all dumped files
                os.remove(path + '/' + file)

    def call_rec_dumper(self, conn, path, data_type, run_count):
        # all files in path
        files = os.listdir(path)

        # traverse recent days according to parameter run_count
        for count in range(1, run_count + 1):

            # get corresponding date
            date = self.get_date(count)

            # extract data from each ".grib" file and dump to database
            for file in files:
                if not os.path.isdir(file) and 'txt' in file and date in file:

                    file = path + '/' + file

                    # call extractor to get dictionary from file
                    grib_extractor = self.call_grib_extractor(data_type, file)

                    # get start time and end time for one record
                    start_time, end_time = self.get_start_end_time(file, date)

                    # dump each (key, value) from extractor's dictionary
                    for key, value in grib_extractor.data.items():

                        lat, long, value = self.rec_value_expand(key, value)

                        # dump temp or mois data if not equals to 'nan'
                        if str(value) != 'nan':
                            self.dumper.insert_one(conn, data_type, p_lat=lat, p_long=long, p_value=value,
                                                    p_start=start_time, p_end=end_time)

                    # remove all dumped files
                    os.remove(path + '/' + file)

    def his_value_expand(self, key):
        # format key into lat, long, time
        lat = float(key[0])
        long = 360 + float(key[1])
        time = key[2]
        return lat, long, time

    def rec_value_expand(self, key, value):
        # format (key, value) into lat, long, value
        lat = float(key[1:key.find(',')])
        long = float(key[key.find(',') + 1:key.find(')')])
        v = float(value)
        return lat, long, v


    def call_tif_extractor(self, path, file):
        # call TIF Extractor
        tif_extractor = TIFExtractor(path + '/' + file)
        tif_extractor.extract()
        return tif_extractor

    def call_grib_extractor(self, data_type, file):
        # call GRIB Extractor
        grib_extractor = GRIBExtractor(file)
        if data_type == MoisTempCrawler.REC_MOIS_MODE:
            grib_extractor.extract(
                prop_name= MoisTempCrawler.MOIS_PROP_NAME,
                prop_first=0, prop_second=10
            )
        elif data_type == MoisTempCrawler.REC_TEMP_MODE:
            grib_extractor.extract(
                prop_name = MoisTempCrawler.TEMP_PROP_NAME,
                prop_typeOfLevel = MoisTempCrawler.TEMP_PROP_TYPEOFLEVEL
            )
        return grib_extractor

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






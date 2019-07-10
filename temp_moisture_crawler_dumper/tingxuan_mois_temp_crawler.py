#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
from urllib.request import urlopen

import requests
import rootpath
from bs4 import BeautifulSoup

rootpath.append()
from configurations import REC_TEMP_MOIS_PATH, HIS_TEMP_PATH

from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from mois_temp_dumper import MoistureTemperatureDumper
from gribextractor import GRIBExtractor
from tifextractor import TIFExtractor

import datetime

import psycopg2


class MoisTempCrawler(CrawlerBase):
    HIS_TEMP_MODE = 0
    HIS_MOIS_MODE = 1
    REC_TEMP_MODE = 2
    REC_MOIS_MODE = 3

    HIS_TEMP_URL = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/'
    HIS_MOIS_URL = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/'
    REC_TEMP_MOIS_URL = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.'

    def start(self, data_type, run_count=1):
        for cur_run_count in range(run_count):  # to deal with crawling once or previous 6 days' data
            date = self.get_crawling_date(cur_run_count)

            if data_type == MoisTempCrawler.HIS_TEMP_MODE:
                path_to_save_files = HIS_TEMP_PATH
                url = MoisTempCrawler.HIS_TEMP_URL

            if data_type == MoisTempCrawler.HIS_MOIS_MODE:
                path_to_save_files = HIS_TEMP_PATH
                url = MoisTempCrawler.HIS_MOIS_URL

            if data_type == MoisTempCrawler.REC_TEMP_MODE or data_type == MoisTempCrawler.REC_MOIS_MODE:
                path_to_save_files = REC_TEMP_MOIS_PATH
                url = MoisTempCrawler.REC_TEMP_MOIS_URL + date + '/'

            while os.path.exists(path_to_save_files + '/error_urls.txt'):
                self.crawl(path_to_save_files, url)
                self.recall_crawl(path_to_save_files)

    def start(self, end_clause=None, data_type=None, path=None, url=None):
        # start crawling information to in-memory structure self.data
        self.crawl(path, url)
        self.recall_crawl(path)
        # call extractor to extract from self.data

        # call dumper to data from self.data to database
        conn = psycopg2.connect(dbname="testdb", user="tester", password="testpassword",
                                host="cloudberry05.ics.uci.edu", port="5432")
        dumper = MoistureTemperatureDumper()
        self.inject_dumper(dumper)

        if 'historical' in path:
            data_time = 'historical'  # 'recent' or 'historical'
        else:
            data_time = 'recent'

        dateCount = 1  # number of days to dump

        self.callDumper(conn, path, data_time, data_type, dateCount)

        # until it reaches the end_clause

    def __getitem__(self, index):
        # get item from in-memory structure self.data
        pass

    def callDumper(self, conn, dump_path, data_time, data_type, dateCount):
        files = os.listdir(dump_path)
        if data_time == 'recent':
            for count in range(1, dateCount + 1):

                curDate = datetime.datetime.today() - datetime.timedelta(days=count)
                formattedDate = curDate.strftime('%y%m%d')
                date = '20' + str(formattedDate)
                for file in files:
                    if not os.path.isdir(file) and 'txt' in file and date in file:
                        file = dump_path + '/' + file
                        if data_type == 'moisture':
                            grib_extractor = GRIBExtractor(file)
                            grib_extractor.extract(
                                prop_name='Liquid volumetric soil moisture (non-frozen)',
                                prop_first=0, prop_second=10
                            )
                        if data_type == 'temperature':
                            grib_extractor = GRIBExtractor(file)
                            grib_extractor.extract(
                                prop_name='Temperature',
                                prop_typeOfLevel='surface'
                            )
                        start_hour = int(file[file.find('.t') + 2:file.find('z')])
                        end_hour = start_hour + int(file[file.find('grbf') + 4:file.find('.grib2')])

                        start_time = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), start_hour, 0, 0)
                        end_time = datetime.datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), end_hour, 0, 0)

                        for key, value in grib_extractor.data.items():
                            lat = float(key[1:key.find(',')])
                            long = float(key[key.find(',') + 1:key.find(')')])
                            value = float(value)
                            if str(value) != 'nan':
                                if data_type == 'temperature':
                                    self.dumper.insert_one(conn, p_lat=lat, p_long=long, p_value=value,
                                                           p_start=start_time,
                                                           p_end=end_time, attri_name='rec_temp')

                                if data_type == 'moisture':
                                    self.dumper.insert_one(conn, p_lat=lat, p_long=long, p_value=value,
                                                           p_start=start_time,
                                                           p_end=end_time, attri_name='rec_mois')

        if data_time == 'historical':
            for file in files:
                print(file)
                if not os.path.isdir(file) and 'tif' in file:

                    tif_extractor = TIFExtractor(dump_path + '/' + file)
                    tif_extractor.extract()

                    for key, value in tif_extractor.data.items():

                        print(key, value)

                        lat = float(key[0])
                        long = 360 + float(key[1])
                        time = key[2]
                        print(time)
                        if str(value) != '-999000000':
                            if data_type == 'temperature':
                                self.dumper.insert_one(conn, p_lat=lat, p_long=long, p_value=float(value), p_time=time,
                                                       attri_name='his_temp')

                            if data_type == 'moisture':
                                self.dumper.insert_one(conn, p_lat=lat, p_long=long, p_value=float(value), p_time=time,
                                                       attri_name='his_mois')
                    os.remove(dump_path + '/' + file)

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

    def get_crawling_date(self, day_count):
        formattedDate = (datetime.datetime.today() - datetime.timedelta(days=day_count)).strftime('%y%m%d')
        date = '20' + str(formattedDate)
        return date

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


if __name__ == '__main__':
    crawler = MoisTempCrawler()
    crawler.start(data_type=MoisTempCrawler.HIS_TEMP_MODE)
    crawler.start(data_type=MoisTempCrawler.HIS_MOIS_MODE)
    crawler.start(data_type=MoisTempCrawler.REC_TEMP_MODE, run_count=1)
    crawler.start(data_type=MoisTempCrawler.REC_TEMP_MODE, run_count=6)
    crawler.start(data_type=MoisTempCrawler.REC_MOIS_MODE, run_count=1)
    crawler.start(data_type=MoisTempCrawler.REC_MOIS_MODE, run_count=6)

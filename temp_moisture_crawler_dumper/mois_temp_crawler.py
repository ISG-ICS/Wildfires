#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
from urllib.request import urlopen

import requests
import rootpath
from bs4 import BeautifulSoup

rootpath.append()
from configurations import REC_TEMP_MOIS_PATH, HIS_MOIS_PATH, HIS_TEMP_PATH

from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from mois_temp_dumper import MoistureTemperatureDumper
from gribextractor import GRIBExtractor
from tifextractor import TIFExtractor

import datetime

import psycopg2

class MoistureTemperatureCrawler(CrawlerBase):

    def start(self, end_clause=None, data_type=None, path=None, url=None):
        # start crawling information to in-memory structure self.data
        # self.crawl(path, url)
        # self.recall_crawl(path)
        # call extractor to extract from self.data

        # call dumper to data from self.data to database
        conn = psycopg2.connect(dbname="testdb", user="tester", password="testpassword",
                                host="cloudberry05.ics.uci.edu", port="5432")
        dumper = MoistureTemperatureDumper()
        self.inject_dumper(dumper)

        if 'historical' in path:
            data_time = 'historical'            # 'recent' or 'historical'
        else:
            data_time = 'recent'

        dateCount = 1                   # number of days to dump

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
                                prop_name = 'Liquid volumetric soil moisture (non-frozen)',
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
                                    self.dumper.insert_one(conn, p_lat=lat, p_long=long, p_value=value, p_start=start_time,
                                                   p_end=end_time, attri_name='rec_temp')

                                if data_type == 'moisture':
                                    self.dumper.insert_one(conn, p_lat=lat, p_long=long, p_value=value, p_start=start_time,
                                                   p_end=end_time, attri_name='rec_mois')

        if data_time == 'historical':
            for file in files:
                print(file)
                if not os.path.isdir(file) and 'tif' in file:

                    tif_extractor = TIFExtractor(dump_path+'/'+file)
                    tif_extractor.extract()

                    for key, value in tif_extractor.data.items():

                        print(key,value)

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
                    os.remove(dump_path+'/'+file)

    def crawl(self, path, url):
        html = urlopen(url)
        bsObj = BeautifulSoup(html, 'html.parser')
        fileList = bsObj.find_all('a')
        for file in fileList:
            fileLink = file.get('href')
            if ('sfluxgrbf' in fileLink and 'idx' not in fileLink
            and int(fileLink[fileLink.find('grbf') + 4: fileLink.find('.grib2')]) <= 6) \
                    or ('tif' in fileLink):
                url_temp = url + fileLink
                print(url_temp)
                start_time = time.process_time()
                req = requests.get(url_temp)
                end_time = time.process_time()

                if not os.path.exists(path):
                    os.makedirs(path)

                if end_time - start_time > 20:
                    with open(path + '/error_urls.txt', 'a') as error_file:
                        error_file.write(url_temp + '\n')
                        continue

                if 'sfluxgrbf' in fileLink:
                    file_date = url[url.find('cdas.') + 5: url.find('cdas.') + 13]
                    with open(path + '/' + fileLink + '_' + file_date + '.txt', 'wb') as file_to_write:
                        file_to_write.write(req.content)

                if 'tif' in fileLink:
                    with open(path + '/' + fileLink, 'wb') as file_to_write:
                        file_to_write.write(req.content)


    def recall_crawl(self, path):
        # recall the error urls in the file and re-download them
        if os.path.exists(path + '/error_urls.txt'):
            for line in open(path + '/error_urls.txt'):

                start_time = time.process_time()
                req = requests.get(line.strip('\n'))
                end_time = time.process_time()

                if not os.path.exists(path):
                    os.makedirs(path)

                if end_time - start_time > 20:
                    with open(path + '/error_urls_new.txt', 'a') as error_file:
                        error_file.write(line)
                        continue

                if 'historical' in path:
                    if 'temp' in line:
                        with open(path + '/' + line[line.find('t.full'):line.find('.tif') + 4], 'wb') as file_to_write:
                            file_to_write.write(req.content)
                    if 'soil' in line:
                        with open(path + '/' + line[line.find('w.full'):line.find('.tif') + 4], 'wb') as file_to_write:
                            file_to_write.write(req.content)

                if 'recent' in path:
                    file_date = line[line.find('cdas.') + 5: line.find('cdas.') + 13]
                    with open(
                            path + '/' + line[line.find('cdas1.'):line.find('.grib2') + 6] + '_' + file_date + '.txt','wb') as file_to_write:
                        file_to_write.write(req.content)
            os.remove(path + '/error_urls.txt')
            if os.path.exists(path + '/error_urls_new.txt'):
                os.rename(path + '/error_urls_new.txt', path + '/error_urls.txt')


if __name__ == '__main__':
    crawler = MoistureTemperatureCrawler()
    crawler.start(data_type='temperature', path=HIS_TEMP_PATH,
                  url='http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/')





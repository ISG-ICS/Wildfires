#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import time
from urllib.request import urlopen

import requests
import rootpath
from bs4 import BeautifulSoup

rootpath.append()
from configurations import REC_TEMP_MOIS_PATH


class MoistureTemperatureCrawler():
    def __init__(self, path):
        self.path = path

    def crawl_data(self, url):
        if 'historical' in self.path:
            html = urlopen(url)
            bsObj = BeautifulSoup(html, 'html.parser')
            fileList = bsObj.find_all('a')
            for file in fileList:
                fileLink = file.get('href')
                if 'tif' in fileLink:
                    url_temp = url + fileLink
                    print(url_temp)

                    start_time = time.process_time()
                    req = requests.get(url_temp)
                    end_time = time.process_time()

                    if not os.path.exists(self.path):
                        os.makedirs(self.path)

                    if end_time - start_time > 10:
                        with open(self.path + '/error_urls.txt', 'a') as error_file:
                            error_file.write(url_temp + '\n')
                            continue

                    with open(self.path + '/' + fileLink, 'wb') as file_to_write:
                        file_to_write.write(req.content)

        if 'recent' in self.path:
            html = urlopen(url)
            bsObj = BeautifulSoup(html, 'html.parser')
            fileList = bsObj.find_all('a')
            for file in fileList:
                fileLink = file.get('href')
                if 'sfluxgrbf' in fileLink and 'idx' not in fileLink and int(
                        fileLink[fileLink.find('grbf') + 4:fileLink.find('.grib2')]) <= 6:
                    url_temp = url + fileLink
                    print(url_temp)
                    start_time = time.process_time()
                    req = requests.get(url_temp)
                    end_time = time.process_time()

                    if not os.path.exists(self.path):
                        os.makedirs(self.path)

                    if end_time - start_time > 20:
                        with open(self.path + '/error_urls.txt', 'a') as error_file:
                            error_file.write(url_temp + '\n')
                            continue

                    file_date = url[url.find('cdas.') + 5:url.find('cdas.') + 13]
                    with open(self.path + '/' + fileLink + '_' + file_date + '.txt', 'wb') as file_to_write:
                        file_to_write.write(req.content)

    def recall_data(self):
        for line in open(self.path + '/error_urls.txt'):

            start_time = time.process_time()
            req = requests.get(line.strip('\n'))
            end_time = time.process_time()

            if not os.path.exists(self.path):
                os.makedirs(self.path)

            if end_time - start_time > 20:
                with open(self.path + '/error_urls_new.txt', 'a') as error_file:
                    error_file.write(line)
                    continue

            if 'historical' in self.path:
                if 'temp' in line:
                    with open(self.path + '/' + line[line.find('t.full'):line.find('.tif') + 4], 'wb') as file_to_write:
                        file_to_write.write(req.content)
                if 'soil' in line:
                    with open(self.path + '/' + line[line.find('w.full'):line.find('.tif') + 4], 'wb') as file_to_write:
                        file_to_write.write(req.content)

            if 'recent' in self.path:
                file_date = line[line.find('cdas.') + 5:line.find('cdas.') + 13]
                with open(
                        self.path + '/' + line[line.find('cdas1.'):line.find('.grib2') + 6] + '_' + file_date + '.txt',
                        'wb') as file_to_write:
                    file_to_write.write(req.content)

        if os.path.exists(self.path + '/error_urls.txt'):
            os.remove(self.path + '/error_urls.txt')
        if os.path.exists(self.path + '/error_urls_new.txt'):
            os.rename(self.path + '/error_urls_new.txt', self.path + '/error_urls.txt')

if __name__ == '__main__':
    # path = path to save data
    # data_time = 'recent' or 'historical'

    # crawl historical moisture data
    # exp = MoistureTemperatureCrawler(HIS_MOIS_PATH)
    # exp.crawl_data('http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/')
    # exp.recall_data()
    # crawl historical temperature data
    # exp = MoistureTemperatureCrawler(HIS_TEMP_PATH)
    # exp.crawl_data('http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/')
    # exp.recall_data()

    # crawl past 6 days of recent data
    # crawler = MoistureTemperatureCrawler(REC_TEMP_MOIS_PATH)
    # for countDate in range(1, 7):
    #     curDate = datetime.datetime.today() - datetime.timedelta(days=countDate)
    #     formattedDate = curDate.strftime('%y%m%d')
    #     date = '20' + str(formattedDate)
    #     crawler.crawl_data('https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/')

    # crawl yesterday's recent data
    crawler = MoistureTemperatureCrawler(REC_TEMP_MOIS_PATH)
    # yesterday = datetime.datetime.today() - datetime.timedelta(days=1).strftime('%y%m%d')
    # date = '20' + str(yesterday)
    # crawler.crawl_data('https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/')
    crawler.recall_data()

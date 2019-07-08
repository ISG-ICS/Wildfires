#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import os
from urllib.request import urlopen

import requests
import rootpath
from bs4 import BeautifulSoup

rootpath.append()
from configurations import REC_TEMP_MOIS_PATH


class MoistureTemperatureCrawler:
    def __init__(self, path, data_time='recent'):
        self.data_time = data_time  # indicate historical or recent data
        self.path = path  # path to save the data

    def crawl_data(self, url, date=0):
        if self.data_time == 'historical':
            html = urlopen(url)
            bsObj = BeautifulSoup(html, 'html.parser')
            fileList = bsObj.find_all('a')
            for file in fileList:
                fileLink = file.get('href')
                if 'tif' in fileLink:
                    url_temp = url + fileLink
                    print(url_temp)
                    req = requests.get(url_temp)
                    if not os.path.exists(self.path):
                        os.makedirs(self.path)
                    with open(self.path + '/' + fileLink, 'wb') as file_to_write:
                        file_to_write.write(req.content)

        if self.data_time == 'recent':
            html = urlopen(url)
            bsObj = BeautifulSoup(html, 'html.parser')
            fileList = bsObj.find_all('a')
            for file in fileList:
                fileLink = file.get('href')
                if 'sfluxgrbf' in fileLink and 'idx' not in fileLink and int(
                        fileLink[fileLink.find('grbf') + 4:fileLink.find('.grib2')]) <= 6:
                    url_temp = url + fileLink
                    print(url_temp)
                    req = requests.get(url_temp)
                    if not os.path.exists(self.path):
                        os.makedirs(self.path)
                    with open(self.path + '/' + fileLink + '_' + date + '.txt', 'wb') as file_to_write:
                        file_to_write.write(req.content)


if __name__ == '__main__':
    # path = path to save data
    # data_time = 'recent' or 'historical'

    # crawl historical moisture data
    # exp = MoistureTemperatureCrawler(HIS_MOIS_PATH, 'historical')
    # exp.crawl_data('http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/')

    # crawl historical temperature data
    # exp = MoistureTemperatureCrawler(HIS_TEMP_PATH, 'historical')
    # exp.crawl_data('http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/')

    # crawl past 6 days of recent data
    exp = MoistureTemperatureCrawler(REC_TEMP_MOIS_PATH, 'recent')
    for countDate in range(1, 7):
        curDate = datetime.datetime.today() - datetime.timedelta(days=countDate)
        formattedDate = curDate.strftime('%y%m%d')
        date = '20' + str(formattedDate)
        exp.crawl_data('https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/', date)

    # crawl yesterday's recent data
    # curDate = datetime.datetime.today()
    # yesterday = curDate.strftime('%y%m%d') - 1
    # date = '20' + str(yesterday)
    # url = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/'
    # exp.crawl_data('https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/')

    # exp = MoistureTemperatureCrawler('historical_temperature_data', 'historical', 'temperature')
    # exp.crawl_data()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup


class MoistureTemperatureCrawler:
    def __init__(self, data_time='recent', data_type='temperature'):
        self.data_time = data_time  # indicate historical or recent data
        self.data_type = data_type  # indicate moisture or temperature

    def crawl_data(self):
        if self.data_time == 'historical':
            if self.data_type == 'moisture':
                html = urlopen('http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/')
                bsObj = BeautifulSoup(html, 'html.parser')
                fileList = bsObj.find_all('a')
                for file in fileList:
                    fileLink = file.get('href')
                    if 'tif' in fileLink:
                        url = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/' + fileLink
                        print(url)
                        req = requests.get(url)
                        with open('./historical_moisture_data/' + fileLink, 'wb') as file_to_write:
                            file_to_write.write(req.content)
            if self.data_type == 'temperature':
                html = urlopen('http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/')
                bsObj = BeautifulSoup(html, 'html.parser')
                fileList = bsObj.find_all('a')
                for file in fileList:
                    fileLink = file.get('href')
                    if 'tif' in fileLink:
                        url = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/temp/total/daily/' + fileLink
                        print(url)
                        req = requests.get(url)
                        with open('./historical_temperature_data/' + fileLink, 'wb') as file_to_write:
                            file_to_write.write(req.content)

        if self.data_time == 'recent':
            for countDate in range(1, 7):  # 6 days of date available
                curDate = datetime.datetime.today() - datetime.timedelta(days=countDate)
                formattedDate = curDate.strftime('%y%m%d')
                date = '20' + str(formattedDate)
                html = urlopen('https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/')
                bsObj = BeautifulSoup(html, 'html.parser')
                fileList = bsObj.find_all('a')
                locations
                count = 1
                for file in fileList:
                    fileLink = file.get('href')
                    if 'sflux' in fileLink and 'idx' not in fileLink and count <= 7:
                        if count == 1:
                            count += 1
                            continue
                        url = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/' + fileLink
                        req = requests.get(url)
                        with open('./recent_moisture_data/' + fileLink + '_' + date + '.txt', 'wb') as file_to_write:
                            file_to_write.write(req.content)
                        count += 1


if __name__ == '__main__':
    # data_time = 'recent' or 'historical', data_type = 'moisture' or 'temperature'
    exp = MoistureTemperatureCrawler('recent', 'moisture')
    exp.crawl_data()

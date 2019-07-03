#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import time
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup


class moisture_crawler:
    def __init__(self, data_type):
        self.data_type = data_type

        today = datetime.date.today()
        formatted_today = today.strftime('%y%m%d')
        yesterday = int(formatted_today) - 1
        date = '20' + str(yesterday)
        self.date = date
        if data_type == 'historical':
            self.html = urlopen('http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/')
        if data_type == 'recent':
            self.html = urlopen('https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/')
        self.bsObj = BeautifulSoup(self.html, 'html.parser')
        self.t1 = self.bsObj.find_all('a')

    def crawl_data(self):
        if self.data_type == 'historical':
            for t2 in self.t1:
                t3 = t2.get('href')
                if 'tif' in t3:
                    url = 'http://ftp.cpc.ncep.noaa.gov/GIS/USDM_Products/soil/total/daily/' + t3
                    print(url)
                    r = requests.get(url)
                    with open('./historical_moisture_data/' + t3, 'wb') as f:
                        f.write(r.content)

        if self.data_type == 'recent':
            count = 1
            for t2 in self.t1:
                t3 = t2.get('href')
                if 'sflux' in t3 and 'idx' not in t3 and count <= 7:
                    if count == 1:
                        count += 1
                        continue
                    url = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + self.date + '/' + t3
                    print(url)
                    r = requests.get(url)
                    time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    with open('./recent_moisture_data/' + t3 + '_' + time_now + '.txt', 'wb') as f:
                        f.write(r.content)
                    count += 1


if __name__ == '__main__':
    exp = moisture_crawler('recent')
    exp.crawl_data()

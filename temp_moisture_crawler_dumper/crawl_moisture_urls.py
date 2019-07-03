import datetime
import time
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup


class moisture_crawler:
    def crawl_moisture(self):
        today = datetime.date.today()
        formatted_today = today.strftime('%y%m%d')
        yesterday = int(formatted_today) - 1
        # more data needed then add loop to the date
        date = '20' + str(yesterday)

        html = urlopen('https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/')
        bsObj = BeautifulSoup(html, 'html.parser')
        t1 = bsObj.find_all('a')

        count = 1
        for t2 in t1:
            t3 = t2.get('href')
            if 'sflux' in t3 and 'idx' not in t3 and count <= 7:
                if count == 1:
                    count += 1
                    continue
                url = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/cfs/prod/cdas.' + date + '/' + t3
                print(url)

                r = requests.get(url)
                # add date to the file name
                time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                with open('./moisture_data/' + t3 + '_' + time_now + '.txt', 'wb') as f:
                    f.write(r.content)
                count += 1


if __name__ == '__main__':
    moisture_crawler().crawl_moisture()

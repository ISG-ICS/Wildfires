import requests
import json
import re
import urllib.request
from bs4 import BeautifulSoup
from connection import Connection
import psycopg2


def truncate_table(table_name):
    conn = Connection()()
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE ' + table_name)
    cur.close()
    conn.commit()


def getTwitterImage(link):
    if requests.get(link).status_code < 400:
        source = urllib.request.urlopen(expandedUrl).read()
        soup = BeautifulSoup(source, 'html.parser')
        imgs = soup.findAll("div", {"class": "AdaptiveMedia-photoContainer js-adaptive-photo"})
        imgUrl = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(imgs))
        uniqueImgUrl = list(set(imgUrl))
        return uniqueImgUrl
    else:
        # print("404 not found")
        return -1


truncate_table('images')

with open("tweets_urls", 'rb') as file:
    data = json.load(file)
    tweetPhoto_dict = dict()  # id: url that contains tweets that have pics
    cnt = 0
    amt = 0
    conn = Connection()()
    for id, item in data.items():
        amt += 1
        if amt % 500  == 0:
            print("ID processed: "+ str(amt) + ", containing images (url): " + str(cnt))
        for element in item:
            try:
                expandedUrl = requests.get(element).url
            
                # in the situation that the url links to a tweet with image
                if (expandedUrl.find("twitter") != -1):
                    # print("the url links to a tweet with photo")
                    photoUrl = getTwitterImage(expandedUrl)
                    if (photoUrl != -1)and(photoUrl!=[]):
                        cnt += 1
                        # print(photoUrl)
                        tweetPhoto_dict.update({id: photoUrl})
                        
                        cur = conn.cursor()
                        insert_query = """insert into images(id,image_url) values(%s,%s)"""
                        for each_link in photoUrl:
                            cur.execute(insert_query, (id, each_link))
                        cur.close()
                        conn.commit()
                        
                break
            except:
                break

    conn.close()
  

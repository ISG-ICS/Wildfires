

import json
import re
import urllib.request

import requests
from bs4 import BeautifulSoup
from url_extract.URL_Classifier import URLClassifier
from data_preparation.connection import Connection


def truncate_table(table_name):
    conn = Connection()()
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE ' + table_name)
    cur.close()
    conn.commit()


def get_ins(url):
    # gets ins image or video url
    try:
        response = requests.get(url)
        if response.status_code < 300:
            all_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                  response.text)
            all_urls_unique = set(all_urls)

            img_urls = [url for url in all_urls_unique if
                        "https://scontent-lax3-1.cdninstagram.com" and "e35" in url and "s150x150" not in url]
            if img_urls == []:
                img_urls = [url for url in all_urls_unique if
                            "https://scontent-lax3-1.cdninstagram.com" and "mp4" in url and "s150x150" not in url]
            final_img_url = img_urls[0]
            return [final_img_url]
        else:
            print('error: ', response.status_code)
            return -1
    except Exception as e:
        print(e)
        return -1


def get_twitter_image(link):
    # gets twitter image ur;
    if requests.get(link).status_code < 300:
        source = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(source, 'html.parser')
        imgs = soup.findAll("div", {"class": "AdaptiveMedia-photoContainer js-adaptive-photo"})
        img_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                             str(imgs))
        unique_img_url = list(set(img_url))
        return unique_img_url
    else:
        return -1


def get_twitter_video(link):
    # gets twitter video url
    from selenium import webdriver
    driver = webdriver.PhantomJS()
    driver.get(link)
    html = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    if requests.get(link).status_code < 300:
        soup = BeautifulSoup(html, 'html.parser')
        imgs = soup.find_all("meta")
        img_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                              str(imgs))
        img_url = [url for url in img_urls if "facebook" in url]
        unique_url = list(set(img_url))
        return unique_url
    else:
        return -1


if __name__ == '__main__':

    # truncate_table('images')
    # start from 10041

    with open("tweets_urls.json", 'rb') as file:
        data = json.load(file)
        tweetPhoto_dict = dict()  # id: url that contains tweets that have pics
        cnt = 0
        amt = 0
        with Connection() as conn:
            for id, item in data.items():
                amt += 1
                print(amt)
                cur = conn.cursor()
                if amt >= 10040:
                    for element in item:
                        print(element)
                        try:
                            link_type = URLClassifier.classify(URLClassifier, element)
                            if link_type == 0:
                                print("link type: twitter, img")
                                photoUrl = get_twitter_image(element)
                            elif link_type == 1:
                                photoUrl = get_twitter_video(element)
                                print("link type: twitter, video")
                            elif link_type == 2:
                                print("link type: ins")
                                photoUrl = get_ins(element)
                            else:
                                photoUrl = -1
                                print("link type: others")
                            if (photoUrl != -1) and (photoUrl != []):
                                cnt += 1
                                print(photoUrl)

                                insert_query = 'insert into images(id,image_url) values (%s, %s)'
                                for each_link in photoUrl:
                                    cur.execute(insert_query, (id, each_link))

                            if amt % 20 == 0:
                                conn.commit()
                        except Exception as err:
                            print("error", err)
                            conn.commit()
                            continue

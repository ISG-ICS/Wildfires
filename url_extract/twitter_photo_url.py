import json
import re
import urllib.request

import requests
from bs4 import BeautifulSoup
from url_extract.URL_Classifier import URLClassifier
from data_preparation.connection import Connection
import webbrowser


def truncate_table(table_name):
    conn = Connection()()
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE ' + table_name)
    cur.close()
    conn.commit()


def get_ins(link):
    # gets ins image or video url
    try:
        response = requests.get(link)
        if response.status_code < 300:
            all_urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                                  response.text)
            all_urls_unique = set(all_urls)
            img_urls = [url for url in all_urls_unique if  # ins image
                        "https://scontent-lax3-1.cdninstagram.com" and "e35" in url and "s150x150" not in url]
            if not img_urls:
                img_urls = [url for url in all_urls_unique if  # ins video
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
        img_url = [url for url in img_urls if "facebook" in url]  # twitter video links usually have keyword "facebook"
        unique_url = list(set(img_url))
        return unique_url
    else:
        return -1


def img_vdo_auto_opener(id, url_list):
    label_dict = dict()
    for each_url in url_list:
        webbrowser.open(each_url)
        label = input("1 for yes, 0 for no")
        label_dict.update({id: (each_url, label)})
    return label_dict


if __name__ == '__main__':

    # truncate_table('images')
    # uncomment the truncate_table line when you need to restart the whole data base uploading process

    # last stopped at 10041

    with open("tweets_urls.json", 'rb') as file:
        data = json.load(file)
        img_vdo_label_dict = dict()
        amt = 0  # counts the number of link processed
        cnt = 0  # the number of pic
        with Connection() as conn:
            for id, item in data.items():
                amt += 1
                print(amt)
                cur = conn.cursor()
                if amt < 500:  # stop at 500
                    for element in item:
                        print("shorten link:", element)

                        try:
                            link_type = URLClassifier.classify(URLClassifier, element)  # classifies link type
                            if link_type == 0:
                                print("link type: twitter, img")
                                photo_url = get_twitter_image(element)
                            elif link_type == 1:
                                print("link type: twitter, video")
                                photo_url = get_twitter_video(element)
                            elif link_type == 2:
                                print("link type: ins")
                                photo_url = get_ins(element)
                            else:
                                print("link type: others")
                                photo_url = -1

                            if (photo_url != -1) and (photo_url != []):
                                print(photo_url)
                                label_dict = img_vdo_auto_opener(id, photo_url)
                                img_vdo_label_dict.update(label_dict)
                                insert_query = 'insert into images(id,image_url) values (%s, %s)'
                                for each_link in photo_url:
                                    cur.execute(insert_query, (id, each_link))
                            json.dump(img_vdo_label_dict, open("media_label.json", "a"))
                            # img_vdo_label_dict.clear()
                            if amt % 20 == 0:
                                conn.commit()
                        except Exception as err:
                            print("error", err)
                            conn.commit()
                            continue

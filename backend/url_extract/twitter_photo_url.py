import errno
import json
import os
import re
import signal
import urllib.request
from functools import wraps

import requests
from bs4 import BeautifulSoup


class TimeoutError(Exception):
    def __init__(self, value="Timed Out"):
        self.value = value

    def __str__(self):
        return repr(self.value)


class TimeoutException(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutException(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


from backend.data_preparation.connection import Connection


def truncate_table(table_name):
    conn = Connection()()
    cur = conn.cursor()
    cur.execute('TRUNCATE TABLE ' + table_name)
    cur.close()
    conn.commit()


@timeout(5)
def get_link_type(short_link):
    expanded_url = requests.get(short_link).url
    print(expanded_url)
    if expanded_url.find("twitter") != -1:
        return 3
    elif expanded_url.find("instagram") != -1:
        return 4
    else:
        return 5


# def get_ins_image(link):
#     print("link")
#     if requests.get(link).status_code < 300:
#         source = urllib.request.urlopen(link).read()
#         soup = BeautifulSoup(source, 'html.parser')
#         imgs = soup.findAll("div", {"class": "AdaptiveMedia-photoContainer js-adaptive-photo"})
#         img_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
#                              str(imgs))
#         unique_img_url = list(set(img_url))
#         return unique_img_url
#     else:
#         # print("404 not found")
#         return -1


def get_twitter_image(link):
    if requests.get(link).status_code < 300:
        source = urllib.request.urlopen(link).read()
        soup = BeautifulSoup(source, 'html.parser')
        imgs = soup.findAll("div", {"class": "AdaptiveMedia-photoContainer js-adaptive-photo"})
        img_url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                             str(imgs))
        unique_img_url = list(set(img_url))
        return unique_img_url
    else:
        # print("404 not found")
        return -1


if __name__ == '__main__':

    truncate_table('images')

    with open("tweets_urls.json", 'rb') as file:
        data = json.load(file)
        tweetPhoto_dict = dict()  # id: url that contains tweets that have pics
        cnt = 0
        amt = 0
        with Connection() as conn:
            for id, item in data.items():
                amt += 1
                print(amt)
                for element in item:
                    print(element)
                    try:
                        link_type = get_link_type(element)
                        if link_type == 3:
                            photoUrl = get_twitter_image(element)
                            # elif link_type == 4:
                            #     photoUrl = get_twitter_image(expandedUrl)
                            # else:
                            #     print("others")
                            if (photoUrl != -1) and (photoUrl != []):
                                cnt += 1
                                print(photoUrl)
                                tweetPhoto_dict.update({id: photoUrl})

                                cur = conn.cursor()
                                insert_query = 'insert into images(id,image_url) values (%s, %s)'
                                for each_link in photoUrl:
                                    cur.execute(insert_query, (id, each_link))
                                cur.close()
                                conn.commit()
                    except Exception as err:
                        print("error", err)
                        continue

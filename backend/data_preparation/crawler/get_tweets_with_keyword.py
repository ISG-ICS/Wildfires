import re
import string
import requests
import twitter
import time
from datetime import datetime
import json
from backend.data_preparation.connection import Connection

# account info can be found on slack
from backend.data_preparation.crawler.crawlerbase import CrawlerBase

api = twitter.Api(consumer_key="",
                  consumer_secret="",
                  access_token_key="",
                  access_token_secret="")



def crawl_content_according_to_keywords(keywords: list):
    # Simulate request from a mac browser
    content_list = []
    for keyword in keywords:
        # allows the input to be a keyword list
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
        }
        resp = requests.get(
            'https://twitter.com/i/search/timeline?f=tweets&vertical=news&q=' + keyword + '%20near%3A\"United%20States\"%20within%3A8000mi&l=en&src=typd',
            headers=headers)
        # Clears all punctuation from raw response body
        tr = str.maketrans("", "", string.punctuation)
        content = str(resp.content)
        content = content.translate(tr)
        content_list.append(content)
    return content_list

# TODO: separate this part into Extractor and Dumper class, injecting to Crawler.
def send_live_tweets(keywords: list, batch_number, hasGeoLocation):  # keywords:list, hasGeoLocation, batch_number,
    cnt = 0
    # to keep track of the # of id
    id_set = set()
    return_dict = []
    id_list = []

    while cnt < batch_number:
        # loops until the number of id collected is greater than the batch number
        content_list = crawl_content_according_to_keywords(keywords)
        for content in content_list:
            for id in re.findall("dataitemid(\d+)", content):
                if id not in id_list:
                    id_list.append(id)
                    cnt += 1

    returned_id = api.GetStatuses(id_list)
    for item in returned_id:
        obj = json.loads(str(item))

        # OPTIMIZE: eliminate code duplication by extracting a function.

        if "place" in obj and obj["id"] not in id_set:
            left = obj["place"]['bounding_box']['coordinates'][0][0]
            right = obj["place"]['bounding_box']['coordinates'][0][2]
            center = [(x + y) / 2.0 for x, y in zip(left, right)]
            id_set.add(obj["id"])
            date = datetime.strptime(obj["created_at"], '%a %b %d %H:%M:%S %z %Y')
            # changes string date into timestamp form
            return_dict.append({"id": id, "created_at": date, "text": obj["text"], "lat": center[1], "long": center[0],
                                "hashtags": obj["hashtags"]})
            insert_one_record(id, date, obj["text"], center[1], center[0], obj["hashtags"])
    if hasGeoLocation:
        return return_dict
    else:
        return returned_id


def insert_one_record(id: int, date: datetime, text: str, lat, long, hash_tag: list):
    # template = f"insert into new_records (id, create_at, text, lat, long, hash_tag) values ({id}, {date}, '{text}', {lat}, {long}, '{hash_tag}');"
    # with Connection() as conn:
    #     cur = conn.cursor()
    #     cur.execute(template)
    #     count = conn.commit()
    Connection().sql_execute(
        f"insert into new_records (id, create_at, text, hash_tag) values ({id}, '{date}', '{text}', "
        f"{', '.join(hash_tag) if hash_tag else 'NULL'});", commit=True)

    # TODO: insert the geo-location to table `locations` instead of `records`;
    # TODO: for testing purpose, please use some temp table like `new_locations`


if __name__ == '__main__':
    t0 = time.time()
    returned_dict = send_live_tweets(['wildfire'], 20, True)
    t = time.time()
    timeCounted = t - t0
    for value in returned_dict:
        print(value)
    insert_one_record("100293033", 20394843920, 'hello', 23.44, 48.22, ['hii'])
    print('time:', timeCounted)

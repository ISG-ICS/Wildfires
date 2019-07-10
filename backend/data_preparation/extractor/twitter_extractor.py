import datetime
import json
from datetime import datetime
from typing import List, Optional, Dict
import rootpath
rootpath.append()

from backend.data_preparation.extractor.extractorbase import ExtractorBase


class TweetExtractor(ExtractorBase):
    def __init__(self):
        super().__init__()
        self.crawler_data: Optional[List] = None
        self.data: list = []
        self.id: int

    def extract(self, data_from_crawler: List[Dict]):
        # extracts useful information after being provided with original tweet data (similar to a filter)
        collected_ids = set()
        extracted_data_list = []

        for tweet_json_string in data_from_crawler:
            tweet = json.loads(str(tweet_json_string))
            id = tweet.get('id')
            if not id:
                continue

            if id not in collected_ids:
                collected_ids.add(id)

                # extracts (filters) the useful information
                date_time = datetime.strptime(tweet["created_at"], '%a %b %d %H:%M:%S %z %Y')
                text = tweet["text"].replace("'", "''")
                hashtags = [tag['text'] for tag in tweet["hashtags"]]
                if tweet.get('place') is not None:
                    top_left, _, bottom_right, _ = tweet["place"]['bounding_box']['coordinates'][0]
                else:
                    top_left = bottom_right = None
                    # where the geolocation does not exist

                extracted_data_list += [
                    {'id': id, 'date_time': date_time, 'text': text, 'hashtags': hashtags, 'top_left': top_left,
                     'bottom_right': bottom_right}]
        self.data = extracted_data_list
        return extracted_data_list
        # stores self.data and returns a reference of it

    def export(self, file_type: str, file_name: str) -> None:
        # for example, json
        replace_list = list(self.data)
        if file_type == 'json':
            for each_extractor_line in replace_list:
                each_extractor_line['date_time'] = str(each_extractor_line['date_time'])
                # json does not accept datetime values, does change it into string
            json.dump(replace_list, open(file_name, 'w'))

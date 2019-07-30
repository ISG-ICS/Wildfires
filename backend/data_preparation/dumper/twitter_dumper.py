import datetime
import logging
import traceback
from typing import List, Dict

import rootpath

rootpath.append()

from backend.data_preparation.connection import Connection

from backend.data_preparation.dumper.dumperbase import DumperBase

logger = logging.getLogger('TaskManager')


class TweetDumper(DumperBase):
    def __init__(self):
        super().__init__()
        self.inserted_locations_count = 0

    def insert(self, data_list: List[Dict]) -> None:
        """inserts the given list into the database"""

        location_string = ""
        record_string = ""
        for data in data_list:

            if data['top_left'] is not None and data['bottom_right'] is not None:
                location_string += f"({data['id']}, {data['top_left'][1]}, {data['top_left'][0]}, " \
                                   f"{data['bottom_right'][1]}, {data['bottom_right'][0]}), "
                self.inserted_locations_count += 1
            record_string += f"({data['id']}, '{data['date_time']}', '{data['text']}', " \
                             f"'{', '.join(data['hashtags']) if data['hashtags'] else None}'), "
            self.inserted_count += 1
        record_string = record_string[:-2]
        location_string = location_string[:-2]

        try:
            # makes sure that the line after 'values' is not empty, and no error exists
            if record_string:
                Connection().sql_execute_commit(
                    f"insert into records (id, create_at, text, hash_tag) values {record_string} "
                    f"on conflict (id) do nothing;")
        except Exception:
            logger.error('error: ' + traceback.format_exc())

        try:
            # makes sure that the line after 'values' is not empty, and no error exists
            if location_string:
                Connection().sql_execute_commit(
                    f"insert into locations (id, top_left_lat,top_left_long,bottom_right_lat,bottom_right_long) "
                    f"values {location_string} on conflict (id) do nothing;")
        except Exception:
            logger.error('error: ' + traceback.format_exc())

    def report_status(self):
        return self.inserted_count, self.inserted_locations_count

    def __str__(self):
        return f'{self.__class__.__name__}{{inserted_records={self.inserted_count}, inserted_location_records={self.inserted_locations_count}}}'

    __repr = __str__


if __name__ == '__main__':
    t = TweetDumper()
    t.insert([{'top_left': (120.0, 80.0), 'bottom_right': (30.5, 40.2), 'id': 12312321312312,
               'date_time': datetime.datetime.now(), 'text': "some testing text", 'hashtags': "tag1, tag2"},
              {'top_left': (130.0, 90.0), 'bottom_right': (40.5, 50.2), 'id': 123123132145235,
               'date_time': datetime.datetime.now(), 'text': "some testing text", 'hashtags': "tag2, tag4"},
              {'top_left': (999.9, 999.9), 'bottom_right': (999.9, 999.9), 'id': 41235644324534,
               'date_time': datetime.datetime.now(), 'text': "some testing text", 'hashtags': "tag2, tag3"}
              ])

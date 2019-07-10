from typing import List, Dict

import rootpath
rootpath.append()

from backend.data_preparation.connection import Connection

# account info can be found on slack
from backend.data_preparation.dumper.dumperbase import DumperBase


class TweetDumper(DumperBase):
    def __init__(self):
        super().__init__()
        self.inserted_locations_count = 0
        # dumper holds no data in memory

    def insert(self, data_list: List[Dict]):

        ids_in_db = set(id for id, in Connection().sql_execute("select id from new_records;"))
        # gets all existing keys in database, make sure no duplicated key id will be enter into the database
        location_string = ""
        record_string = ""
        for data in data_list:
            if data['id'] not in ids_in_db:
                if data['top_left'] != None and data['bottom_right'] != None:
                    location_string += f"({data['id']}, {data['top_left'][0]}, {data['top_left'][1]}, " \
                        f"{data['bottom_right'][0]}, {data['bottom_right'][1]}), "
                    self.inserted_locations_count += 1
                record_string += f"({data['id']}, '{data['date_time']}', '{data['text']}', '{', '.join(data['hashtags']) if data['hashtags'] else 'NULL'}'), "
                self.inserted_count += 1
        record_string = record_string[:-2]
        location_string = location_string[:-2]

        try:
            # makes sure that the line after 'values' is not empty, and no error exists
            if record_string:
                Connection().sql_execute_commit(
                    f"insert into new_records (id, create_at, text, hash_tag) values {record_string};")
        except Exception as e:
            print('Error:', e)

        try:
            # makes sure that the line after 'values' is not empty, and no error exists
            if location_string:
                Connection().sql_execute_commit(
                    f"insert into new_locations (id, top_left_lat,top_left_long,bottom_right_lat,bottom_right_long) values {location_string};")
        except Exception as e:
            print('Error:', e)

    def report_status(self):
        return self.inserted_count, self.inserted_locations_count

    def __str__(self):
        return f'{self.__class__.__name__}{{inserted_records={self.inserted_count}, inserted_location_records={self.inserted_locations_count}}}'

    __repr = __str__


# if __name__ == '__main__':
#     t = TweetDumper()
#     t.insert([{'top_left': (120.0, 80.0), 'bottom_right': (30.5, 40.2), 'id': 12312321312312,
#                'date_time': datetime.datetime.now(), 'text': "some testing text", 'hashtags': "tag1, tag2"},
#               {'top_left': (130.0, 90.0), 'bottom_right': (40.5, 50.2), 'id': 123123132145235,
#                'date_time': datetime.datetime.now(), 'text': "some testing text", 'hashtags': "tag2, tag4"},
#               {'top_left': (999.9, 999.9), 'bottom_right': (999.9, 999.9), 'id': 41235644324534,
#                'date_time': datetime.datetime.now(), 'text': "some testing text", 'hashtags': "tag2, tag3"}
#               ])

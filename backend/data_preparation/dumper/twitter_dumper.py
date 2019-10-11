import datetime
import logging
import traceback
from typing import List, Dict

import rootpath
from psycopg2 import extras

rootpath.append()

from backend.connection import Connection

from backend.data_preparation.dumper.dumperbase import DumperBase

logger = logging.getLogger('TaskManager')


class TweetDumper(DumperBase):
    def __init__(self):
        super().__init__()
        self.inserted_locations_count = 0
        self.inserted_count = 0

    def insert(self, data_list: List[Dict]) -> None:
        """inserts the given list into the database"""
        # construct sql statement to insert data into the records db table
        tuples_records = []
        for data in data_list:
            tuples_records += [(data['id'], data['date_time'], data['full_text'],
                                ', '.join(data['hashtags']) if data['hashtags'] else None, data['profile_pic'],
                                data['created_date_time'], data['screen_name'], data['user_name'],
                                data['followers_count'],
                                data['favourites_count'], data['friends_count'], data['user_id'], data['user_location'],
                                data['statuses_count'])]
            self.inserted_count += 1

        try:
            with Connection() as connection:
                cur = connection.cursor()
                if tuples_records:
                    extras.execute_values(cur,
                                          f"insert into records (id,create_at, text, hash_tag,profile_pic,created_date_time,screen_name,"
                                          f"user_name,followers_count,favourites_count,friends_count,user_id,user_location,statuses_count"
                                          f") values %s "
                                          f"ON CONFLICT(id) DO UPDATE set text = excluded.text, profile_pic = excluded.profile_pic, "
                                          f"screen_name = excluded.screen_name, user_name = excluded.user_name, "
                                          f"followers_count = excluded.followers_count, favourites_count = excluded.favourites_count, "
                                          f"friends_count= excluded.friends_count, user_id= excluded.user_id, user_location= excluded.user_location, "
                                          f" statuses_count= excluded.statuses_count;", tuples_records)
                # if the data is fetched from db and reprocessed, the values will be updated with the help of the ON CONFLICT DO UPDATE
                # if the data is just crawled, the sql statement will just simply insert data into db
                connection.commit()
                cur.close()
        except Exception as err:
            logger.error(str(err) + traceback.format_exc())
        else:
            logger.info(f'data inserted into records {self.inserted_count}')
        # construct sql statement to insert data into the locations db table
        tuples_locations: list[tuple] = []
        for data in data_list:
            if data['top_left'] is not None and data['bottom_right'] is not None:
                tuples_locations += [(data['id'], data['top_left'][1], data['top_left'][0], data['bottom_right'][1],
                                      data['bottom_right'][0])]
                self.inserted_locations_count += 1

        try:
            with Connection() as connection:
                cur = connection.cursor()
                if tuples_locations:
                    extras.execute_values(cur,
                                          f"insert into locations (id, top_left_lat, top_left_long, bottom_right_lat,"
                                          f"bottom_right_long) values %s "
                                          f"ON CONFLICT(id) DO NOTHING;", tuples_locations)
                connection.commit()
                cur.close()
        except Exception as err:
            logger.error(str(err) + traceback.format_exc())
        else:
            logger.info(f'data inserted into locations {self.inserted_locations_count}')

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

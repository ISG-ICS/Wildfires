import datetime
import logging
import traceback
from typing import List, Dict, Tuple

import rootpath
from psycopg2 import extras

rootpath.append()

from backend.connection import Connection

from backend.data_preparation.dumper.dumperbase import DumperBase

logger = logging.getLogger('TaskManager')


class TweetDumper(DumperBase):
    INSERT_WITH_LOCATION_QUERY = f"insert into records (id, create_at, text, hash_tag, profile_pic, " \
                                 f"created_date_time, screen_name, user_name, followers_count, favourites_count, " \
                                 f"friends_count, user_id, user_location, statuses_count, location) " \
                                 f"values %s " \
                                 f"ON CONFLICT(id) DO UPDATE " \
                                 f"set text = excluded.text, profile_pic = excluded.profile_pic, " \
                                 f"screen_name = excluded.screen_name, user_name = excluded.user_name, " \
                                 f"followers_count = excluded.followers_count, " \
                                 f"favourites_count = excluded.favourites_count, " \
                                 f"friends_count= excluded.friends_count, user_id= excluded.user_id, " \
                                 f"user_location= excluded.user_location, " \
                                 f" statuses_count= excluded.statuses_count, location = excluded.location;"

    INSERT_WITHOUT_LOCATION_QUERY = f"insert into records (id, create_at, text, hash_tag, profile_pic, " \
                                    f"created_date_time, screen_name, user_name, followers_count, favourites_count, " \
                                    f"friends_count, user_id, user_location, statuses_count) " \
                                    f"values %s " \
                                    f"ON CONFLICT(id) DO UPDATE " \
                                    f"set text = excluded.text, profile_pic = excluded.profile_pic, " \
                                    f"screen_name = excluded.screen_name, user_name = excluded.user_name, " \
                                    f"followers_count = excluded.followers_count, " \
                                    f"favourites_count = excluded.favourites_count, " \
                                    f"friends_count= excluded.friends_count, user_id= excluded.user_id, " \
                                    f"user_location= excluded.user_location, " \
                                    f" statuses_count= excluded.statuses_count;"

    def __init__(self):
        super().__init__()
        self.inserted_locations_count = 0
        self.inserted_count = 0

    @staticmethod
    def _insert_ids(ids=List[Tuple[int]]):
        """insert given id list into the database"""
        logger.info("Inserting ids")
        with Connection() as connection:
            cur = connection.cursor()
            extras.execute_values(cur, "insert into records (id) values %s on conflict(id) do nothing", ids)
            connection.commit()
            cur.close()

    def insert(self, data_list: List[Dict], id_mode=False) -> None:
        """inserts the given list into the database"""
        # construct sql statement to insert data into the records db table
        if id_mode:
            # only insert ids without other data when id_mode == True
            self._insert_ids([(dic['id'],) for dic in data_list])
        else:
            records_with_location = []
            records_without_location = []
            for data in data_list:
                if data['top_left'] is not None and data['bottom_right'] is not None:
                    # form tuples for data with locations
                    long_tl, lat_tl = data['top_left']
                    long_br, lat_br = data['bottom_right']
                    long = (long_tl + long_br) / 2
                    lat = (lat_br + lat_tl) / 2
                    geom, = next(Connection.sql_execute(f'select st_makepoint({long},{lat})'))
                    records_with_location.append((data['id'], data['date_time'], data['full_text'],
                                                  ', '.join(data['hashtags']) if data['hashtags'] else None,
                                                  data['profile_pic'],
                                                  data['created_date_time'], data['screen_name'], data['user_name'],
                                                  data['followers_count'], data['favourites_count'],
                                                  data['friends_count'],
                                                  data['user_id'], data['user_location'], data['statuses_count'], geom))

                else:
                    records_without_location.append((data['id'], data['date_time'], data['full_text'],
                                                     ', '.join(data['hashtags']) if data['hashtags'] else None,
                                                     data['profile_pic'],
                                                     data['created_date_time'], data['screen_name'], data['user_name'],
                                                     data['followers_count'], data['favourites_count'],
                                                     data['friends_count'],
                                                     data['user_id'], data['user_location'], data['statuses_count']))



            try:
                with Connection() as connection:
                    cur = connection.cursor()
                    if records_with_location:
                        extras.execute_values(cur, self.INSERT_WITH_LOCATION_QUERY, records_with_location)
                        self.inserted_locations_count += cur.rowcount

                    if records_without_location:
                        extras.execute_values(cur, self.INSERT_WITHOUT_LOCATION_QUERY, records_without_location)
                        self.inserted_count += cur.rowcount
                    # if the data is fetched from db and reprocessed,
                    # the values will be updated with the help of the ON CONFLICT DO UPDATE
                    # if the data is just crawled, the sql statement will just simply insert data into db
                    connection.commit()
                    cur.close()
            except Exception as err:
                logger.error(str(err) + traceback.format_exc())
            else:
                logger.info(f'Total data inserted into records: {self.inserted_count}, '
                            f'Total data with locations inserted into records: {self.inserted_locations_count}')

    def report_status(self):
        return self.inserted_count, self.inserted_locations_count

    def __str__(self):
        return f'{self.__class__.__name__}{{inserted_records={self.inserted_count}, ' \
               f'inserted_location_records={self.inserted_locations_count}}}'

    __repr__ = __str__


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    tweet_dumper = TweetDumper()

    # id mode tests:
    tweet_dumper.insert([{'id': 114578942456235}, {'id': 908436598589243}, {'id': 459872893571623}], id_mode=True)

    # normal mode tests:
    extracted_tweets = [{'id': 1192227287204290560,
                         'date_time': datetime.datetime(2019, 11, 6, 23, 48, 30, tzinfo=datetime.timezone.utc),
                         'full_text': '@patheticell The fire wings were reworked, those hairs were the first hairs anyway and even '
                                      'if they were stolen they are 2, almost 3 years old and I\'m pretty sure there\'s this thing '
                                      'called "making mistakes" so Grotty shouldn\'t really be doing this.',
                         'hashtags': [], 'top_left': None, 'bottom_right': None,
                         'profile_pic': 'http://pbs.twimg.com/profile_images/1190851982468227072/cQlsQDXP_normal.jpg',
                         'screen_name': 'ShelbyDreammm', 'user_name': "Shelby - wow it's turkey season",
                         'created_date_time': datetime.datetime(2019, 8, 10, 1, 4, 31, tzinfo=datetime.timezone.utc),
                         'followers_count': 155, 'favourites_count': 785, 'friends_count': 127,
                         'user_id': 1159993896425971712,
                         'user_location': 'None', 'statuses_count': 1830},

                        {'id': 1191824904087330816,
                         'date_time': datetime.datetime(2019, 11, 5, 21, 9, 34, tzinfo=datetime.timezone.utc),
                         'full_text': '12 years ago, Call of Duty 4: Modern Warfare dropped.\n\nA legendary campaign. An iconic '
                                      'game 🙏 https://t.co/HuId8jqPYB',
                         'hashtags': [], 'top_left': None, 'bottom_right': None,
                         'profile_pic': 'http://pbs.twimg.com/profile_images/854437887856791552/kwG7J7_A_normal.jpg',
                         'screen_name': 'BRGaming', 'user_name': 'B/R Gaming',
                         'created_date_time': datetime.datetime(2016, 5, 12, 4, 40, 49, tzinfo=datetime.timezone.utc),
                         'followers_count': 134040, 'favourites_count': 374,
                         'friends_count': 630, 'user_id': 730618709593739264,
                         'user_location': 'de_bleacher', 'statuses_count': 4524},

                        {'id': 1192227303805206529,
                         'date_time': datetime.datetime(2019, 11, 6, 23, 48, 34, tzinfo=datetime.timezone.utc),
                         'full_text': '@Sweeney_Boo My horror tastes tend toward dread-soaked, atmospheric, and ambiguous, '
                                      'so YMMV, but a few I’ve really liked recently are Windeye by Brian Evenson, Things We Lost '
                                      'In the Fire by Mariana Enriquez (unrelated to the movie of the same name), and Mouthful of '
                                      'Birds by Samanta Schweblin.',
                         'hashtags': [], 'top_left': None, 'bottom_right': None,
                         'profile_pic': 'http://pbs.twimg.com/profile_images/1182895421472964609/rj7WQ-rA_normal.jpg',
                         'screen_name': 'nancyreagan2000', 'user_name': 'Steve Wilcox',
                         'created_date_time': datetime.datetime(2013, 6, 17, 22, 47, 53, tzinfo=datetime.timezone.utc),
                         'followers_count': 50, 'favourites_count': 2421, 'friends_count': 419, 'user_id': 1526072742,
                         'user_location': 'None', 'statuses_count': 253},

                        {'id': 1192227271983214593,
                         'date_time': datetime.datetime(2019, 11, 6, 23, 48, 26, tzinfo=datetime.timezone.utc),
                         'full_text': '@BlvckKennedy Looks like you need to go fire yours miss bitch https://t.co/b1yzUpwDFw',
                         'hashtags': [], 'top_left': [-94.406743, 32.491967],
                         'bottom_right': [-94.29016, 32.571239],
                         'profile_pic': 'http://pbs.twimg.com/profile_images/1191575541796757504/_JmOUeWo_normal.jpg',
                         'screen_name': 'CourtneeMaxey',
                         'user_name': 'young tender',
                         'created_date_time': datetime.datetime(2019, 4, 22, 10, 42, 25, tzinfo=datetime.timezone.utc),
                         'followers_count': 442, 'favourites_count': 6072,
                         'friends_count': 385, 'user_id': 1120276663210737669,
                         'user_location': 'Marshall, TX', 'statuses_count': 9450}]
    tweet_dumper.insert(extracted_tweets)

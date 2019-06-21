import json

import psycopg2

from connection import Connection


class Dumper:
    RECORD = 0
    LOCATION = 1

    def __init__(self, json_filename):
        with open(json_filename, 'rb') as file:
            self.tweets = json.load(file)
        self.target_fields = ["id", "bounding_box"]
        self.conn = Connection()()

    def __iter__(self, target):
        if target == Dumper.LOCATION:
            for tweet in self.tweets:
                (a, b), (c, d) = tweet['place']["bounding_box"]
                yield tuple([tweet['id'], a, b, c, d])

        elif target == Dumper.RECORD:
            for tweet in self.tweets:
                yield tuple([tweet[field] for field in ["id", "create_at", "text"]])

    def dump_all(self, table, value_count):
        try:
            sql = f'INSERT INTO {table} VALUES({"%s " * value_count});'
            for record in self:
                print(record)
                cur = self.conn.cursor()
                cur.execute(sql, record)
                cur.close()
                self.conn.commit()

        except psycopg2.DatabaseError as error:
            print(error)

    def get_location(self):
        pass


if __name__ == '__main__':
    dumper = Dumper("../data/tweets/test.json")
    # dumper.dump_all("records", 3)
    # dumper.dump_all("locations", 5)

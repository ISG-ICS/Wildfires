import json

import psycopg2

from connection import Connection


class Dumper:
    def __init__(self, json_filename):
        with open(json_filename, 'rb') as file:
            self.records = json.load(file)
        self.target_fields = ["id", "create_at", "text"]
        self.conn = Connection()()

    def __iter__(self):
        for record in self.records:
            yield tuple([record[field] for field in self.target_fields])

    def dump_all(self):
        try:
            cur = self.conn.cursor()
            sql = 'INSERT INTO records VALUES(%s, %s, %s);'
            for record in self:
                print(record)
                cur.execute(sql, record)
            cur.close()
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            print(error)


if __name__ == '__main__':
    dumper = Dumper("../data/tweets/test.json")
    dumper.dump_all()

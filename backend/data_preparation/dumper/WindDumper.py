from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection
from configurations import WIND_DATA_DIR
import os
import json
import psycopg2.errors


class WindDumper(DumperBase):
    sql_insert = 'INSERT INTO "wind" (reftime, numberpoints, nx, ny, uri) VALUES (%s, %s, %s, %s, %s)'

    def __init__(self):
        super().__init__()

    @staticmethod
    def insert_one(stamp: str, saved_path: str):
        # insert one record into database
        # recording insert count number to self.inserted_count
        with open(os.path.join(WIND_DATA_DIR, stamp + '.json'), 'r') as f:
            json_data = json.load(f)
        for var in json_data:
            refTime = var['header']['refTime']
            numberPoints = var['header']['numberPoints']
            nx = var['header']['nx']
            ny = var['header']['ny']

            with Connection() as conn:
                cur = conn.cursor()
                try:
                    cur.execute(WindDumper.sql_insert, (refTime, numberPoints, nx, ny, saved_path + stamp + '.json'))
                except psycopg2.errors.UniqueViolation:
                    print('\n\tDuplicated Key')
                else:
                    print('Affected rows: ' + str(cur.rowcount))
                if cur.rowcount == 1:
                    conn.commit()
                cur.close()

            break  # only exec once

    @staticmethod
    def insert_batch(*args, **kwargs):
        # insert a batch of records into database
        # recording insert count number to self.inserted_count
        pass


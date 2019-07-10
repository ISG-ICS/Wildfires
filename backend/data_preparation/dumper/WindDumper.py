from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection
from configurations import WIND_DATA_DIR
import os
import json
import psycopg2.errors
import numpy as np


class WindDumper(DumperBase):
    sql_insert = 'INSERT INTO "wind" (reftime, numberpoints, nx, ny, parameter_category, parameter_number\
    , lo1,lo2,la1,la2,dx,dy,mat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

    def __init__(self):
        super().__init__()

    def insert_one(self, stamp: str):
        # insert one record into database
        # recording insert count number to self.inserted_count
        with open(os.path.join(WIND_DATA_DIR, stamp + '.json'), 'r') as f:
            json_data = json.load(f)
        with Connection() as conn:
            for var in json_data:
                refTime = var['header']['refTime']
                numberPoints = var['header']['numberPoints']
                nx = var['header']['nx']
                ny = var['header']['ny']
                parameterCategory = var['header']['parameterCategory']
                parameterNumber = var['header']['parameterNumber']
                lo1 = var['header']['lo1']
                lo2 = var['header']['lo2']
                la1 = var['header']['la1']
                la2 = var['header']['la2']
                dx = var['header']['dx']
                dy = var['header']['dy']
                mat = np.array(var['data'], dtype='float32').reshape((nx, ny))  # type:np.ndarray

                cur = conn.cursor()
                try:
                    cur.execute(WindDumper.sql_insert, (refTime, numberPoints, nx, ny,
                                                        parameterCategory, parameterNumber,
                                                        lo1, lo2, la1, la2, dx, dy, mat.tostring()))
                except psycopg2.errors.UniqueViolation:
                    print('\n\tDuplicated Key')
                else:
                    self.inserted_count = cur.rowcount
                    print('Affected rows: ' + str(cur.rowcount))

            conn.commit()
            cur.close()

    def insert_batch(*args, **kwargs):
        # insert a batch of records into database
        # recording insert count number to self.inserted_count
        pass

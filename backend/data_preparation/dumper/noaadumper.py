from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection
import psycopg2.errors
import psycopg2.extras
import datetime


class NOAADumper(DumperBase):
    sql_insert = 'INSERT INTO "noaa0p25" (tid, gid, ugnd, vgnd, tmp) VALUES %s'
    sql_insert_time = 'INSERT INTO "noaa0p25_reftime" (reftime, tid) VALUES (%s, %s)'

    def __init__(self):
        super().__init__()

    def insert(self, ugnd: dict, vgnd: dict, tmp: dict, reftime: datetime, stamp: str):
        # insert one record into database
        # recording insert count number to self.inserted_count

        with Connection() as conn:
            cur = conn.cursor()
            tid = int(stamp)

            # load data
            data = list()
            gid = 0
            for key in ugnd.keys():
                data.append((tid, gid, ugnd.get(key) + 0.0, vgnd.get(key) + 0.0, tmp.get(key) + 0.0))  # testing
                # data.append(('POINT({} {})'.format(tup[0], tup[1]), gid))  # create geometry mesh
                gid += 1

            # insert data
            try:
                cur.execute(NOAADumper.sql_insert_time, (reftime, tid))
                psycopg2.extras.execute_values(cur, NOAADumper.sql_insert, data, template=None, page_size=10000)
            except psycopg2.errors.UniqueViolation:
                print('\n\tDuplicated Key')
            else:
                self.inserted_count = cur.rowcount
                print('Affected rows: ' + str(cur.rowcount))

            conn.commit()
            cur.close()

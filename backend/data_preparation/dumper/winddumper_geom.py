from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection
import psycopg2.errors
import psycopg2.extras


class WindDumperGeom(DumperBase):
    sql_insert = 'INSERT INTO "wind" (tid, gid, ugnd, vgnd) VALUES %s'
    # sql_select_time = 'SELECT max(tid) from "wind_reftime"'
    # sql_insert_time = 'INSERT INTO "wind_reftime" (reftime, tid) VALUES (%s, %s)'

    def __init__(self):
        super().__init__()

    def insert_one(self, ugnd: dict, vgnd: dict, stamp: str):
        # insert one record into database
        # recording insert count number to self.inserted_count

        with Connection() as conn:
            cur = conn.cursor()
            tid = int(stamp)

            # load data
            data = list()
            gid = 0
            for key in ugnd.keys():
                data.append((tid, gid, ugnd.get(key) + 0.0, vgnd.get(key) + 0.0))  # testing
                # data.append(('POINT({} {})'.format(tup[0], tup[1]), gid))  # wind_geometry
                gid += 1

            # insert wind data
            try:
                # cur.execute(WindDumperGeom.sql_insert_time, (reftime, tid))
                psycopg2.extras.execute_values(cur, WindDumperGeom.sql_insert, data, template=None, page_size=10000)
                # cur.execute(WindDumperGeom.sql_insert, (
                #     3389, json_data[0]['data'][999], json_data[1]['data'][999], 'POINT({} {})'.format(255, 600),
                #     refTime))
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

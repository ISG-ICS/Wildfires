from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection
import psycopg2.errors
import psycopg2.extras
import datetime
from ast import literal_eval as make_tuple


class NOAADumper(DumperBase):
    sql_check_geom = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'noaa0p25_geometry\''
    sql_check_geom2 = 'SELECT * FROM noaa0p25_geometry WHERE gid=0'
    sql_create_geom = 'CREATE TABLE IF NOT EXISTS noaa0p25_geometry (geom geometry, gid int4)'
    sql_insert_geom = 'INSERT INTO noaa0p25_geometry (geom, gid) VALUES %s'
    sql_insert = 'INSERT INTO "noaa0p25" (tid, gid, ugnd, vgnd, tmp, soilw) VALUES %s'
    sql_insert_time = 'INSERT INTO "noaa0p25_reftime" (reftime, tid) VALUES (%s, %s)'

    def __init__(self):
        super().__init__()

    def insert(self, ugnd: dict, vgnd: dict, tmp: dict, soilw: dict, reftime: datetime, stamp: str):

        with Connection() as conn:
            self.check_geom(conn, ugnd)  # create mesh if not exist

            tid = int(stamp)
            data = NOAADumper.data_gen(tid, soilw, tmp, ugnd, vgnd)  # data generator

            # insert data
            try:
                cur = conn.cursor()
                cur.execute(NOAADumper.sql_insert_time, (reftime, tid))
                psycopg2.extras.execute_values(cur, NOAADumper.sql_insert, data, template=None, page_size=10000)
            except psycopg2.errors.UniqueViolation:
                print('\n\tDuplicated Key')
            else:
                self.inserted_count = cur.rowcount
                print('Affected rows: ' + str(cur.rowcount))
                conn.commit()
            finally:
                cur.close()

    def check_geom(self, conn, ugnd: dict) -> None:
        """create geometry table if not exist"""
        cur = conn.cursor()
        # if table not exist
        cur.execute(self.sql_check_geom)
        tables = cur.fetchall()
        if len(tables) == 0:
            cur.execute(NOAADumper.sql_create_geom)
            conn.commit()

        # if table is empty
        cur.execute(self.sql_check_geom2)
        geoms = cur.fetchall()
        if len(geoms) == 0:
            mesh = NOAADumper.geom_gen(ugnd)
            psycopg2.extras.execute_values(cur, NOAADumper.sql_insert_geom, mesh, template=None, page_size=10000)
            conn.commit()
        cur.close()
        return cur

    @staticmethod
    def data_gen(tid: int, soilw: dict, tmp: dict, ugnd: dict, vgnd: dict) -> tuple:
        """generator: data"""
        gid = 0
        for key in ugnd.keys():
            data = (tid, gid, ugnd.get(key) + 0.0, vgnd.get(key) + 0.0, tmp.get(key) + 0.0,
                    soilw.get(key) + 0.0)

            yield data
            gid += 1

    @staticmethod
    def geom_gen(ugnd: dict) -> tuple:
        """generator: geometry"""
        gid = 0
        for key in ugnd.keys():
            tup = make_tuple(key)
            geom = ('POINT({} {})'.format(tup[0], tup[1]), gid)

            yield geom
            gid += 1

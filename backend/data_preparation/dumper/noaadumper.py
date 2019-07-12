from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection
import psycopg2.errors
import psycopg2.extras
import datetime
from ast import literal_eval as make_tuple


class NOAADumper(DumperBase):
    sql_check_geom = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'noaa0p25_geometry\''
    sql_create_geom = 'CREATE TABLE IF NOT EXISTS noaa0p25_geometry (geom geometry, gid int4)'
    sql_insert_geom = 'INSERT INTO noaa0p25_geometry (geom, gid) VALUES %s'
    sql_insert = 'INSERT INTO "noaa0p25" (tid, gid, ugnd, vgnd, tmp, soilw) VALUES %s'
    sql_insert_time = 'INSERT INTO "noaa0p25_reftime" (reftime, tid) VALUES (%s, %s)'

    def __init__(self):
        super().__init__()

    def insert(self, ugnd: dict, vgnd: dict, tmp: dict, soilw: dict, reftime: datetime, stamp: str):

        with Connection() as conn:
            self.check_mesh(conn, ugnd)  # create mesh if not exist

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

    # create mesh if not exist
    def check_mesh(self, conn, ugnd: dict) -> None:
        cur = conn.cursor()
        cur.execute(self.sql_check_geom)
        tables = cur.fetchall()
        if len(tables) == 0:
            cur.execute(NOAADumper.sql_create_geom)
            mesh = NOAADumper.mesh_gen(ugnd)
            psycopg2.extras.execute_values(cur, NOAADumper.sql_insert_geom, mesh, template=None, page_size=10000)
            conn.commit()
        cur.close()
        return cur

    # generator: data
    @staticmethod
    def data_gen(tid: int, soilw: dict, tmp: dict, ugnd: dict, vgnd: dict) -> tuple:
        gid = 0
        for key in ugnd.keys():
            data = (tid, gid, ugnd.get(key) + 0.0, vgnd.get(key) + 0.0, tmp.get(key) + 0.0,
                    soilw.get(key) + 0.0)

            yield data
            gid += 1

    # generator: mesh
    @staticmethod
    def mesh_gen(ugnd: dict) -> tuple:
        gid = 0
        for key in ugnd.keys():
            tup = make_tuple(key)
            mesh = ('POINT({} {})'.format(tup[0], tup[1]), gid)

            yield mesh
            gid += 1

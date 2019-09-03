import datetime
import logging
from ast import literal_eval as make_tuple
from typing import Tuple, Generator

import psycopg2.errors
import psycopg2.extras

from utilities.connection import Connection
from .dumperbase import DumperBase

logger = logging.getLogger('TaskManager')


class NOAADumper(DumperBase):
    sql_check_geom = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'noaa0p25_geometry\''
    sql_check_geom2 = 'SELECT * FROM noaa0p25_geometry WHERE gid=0'
    sql_create_geom = 'CREATE TABLE IF NOT EXISTS noaa0p25_geometry (geom geometry, gid int4)'
    sql_insert_geom = 'INSERT INTO noaa0p25_geometry (geom, gid) VALUES %s'
    sql_insert = 'INSERT INTO "noaa0p25" (tid, gid, ugnd, vgnd, tmp, soilw) VALUES %s ' \
                 'ON CONFLICT (tid, gid) DO UPDATE SET ' \
                 'ugnd = EXCLUDED.ugnd, vgnd = EXCLUDED.vgnd, tmp=EXCLUDED.tmp, soilw=EXCLUDED.soilw'
    sql_insert_time = 'INSERT INTO "noaa0p25_reftime" (reftime, tid) VALUES (%s, %s)'

    def __init__(self):
        super().__init__()

    def insert(self, ugnd: dict, vgnd: dict, tmp: dict, soilw: dict, reftime: datetime, stamp: str) -> None:

        with Connection() as conn:
            self.check_geom(conn, ugnd)  # create mesh if not exist

            tid = int(stamp)
            data = NOAADumper.data_gen(tid, soilw, tmp, ugnd, vgnd)  # data generator

            # insert data
            try:
                cur = conn.cursor()
                cur.execute(NOAADumper.sql_insert_time, (reftime, tid))
                psycopg2.extras.execute_values(cur, NOAADumper.sql_insert, data, template=None, page_size=10000)

            # FIXME: when will this error happen? does it terminate at the error point? also not able to find error
            #  reference to `psycopg2.errors.UniqueViolation`
            except psycopg2.errors.UniqueViolation:
                logger.error('\n\tDuplicated Key')
            else:
                self.inserted_count = cur.rowcount
                logger.info('affected records: ' + str(cur.rowcount))
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
        if not len(geoms):
            mesh = NOAADumper.geom_gen(ugnd)
            psycopg2.extras.execute_values(cur, NOAADumper.sql_insert_geom, mesh, template=None, page_size=10000)
            conn.commit()
        cur.close()

    @staticmethod
    def data_gen(tid: int, soilw: dict, tmp: dict, ugnd: dict, vgnd: dict) -> Generator[
        Tuple[int, int, float, float, float, float], None, None]:
        """generator: data"""
        gid = 0
        for key in ugnd.keys():
            yield tid, gid, ugnd.get(key) + 0.0, vgnd.get(key) + 0.0, tmp.get(key) + 0.0, soilw.get(key) + 0.0
            gid += 1

    @staticmethod
    def geom_gen(ugnd: dict) -> Generator[Tuple[str, int], None, None]:
        """generator: geometry"""
        gid = 0
        for key in ugnd.keys():
            x, y = make_tuple(key)
            yield f'POINT({x} {y})', gid
            gid += 1

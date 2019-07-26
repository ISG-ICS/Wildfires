from typing import List, Dict

import rootpath
rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection

class FireDumper(DumperBase):
    """
    Table 1(fire_crawl_history): fireyear firename
    Table 2(fire_geoms): firename firetime firegeom
    """
    sql_check_if_history_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_crawl_history\''
    sql_retrieve_all_fires = 'SELECT * FROM fire_names'
    sql_create_history_table = 'CREATE TABLE IF NOT EXISTS fire_crawl_history (fireyear int4, firename VARCHAR (30))'
    def __init__(self):
        super().__init__()

    def insert(self, ugnd: dict, vgnd: dict, tmp: dict, soilw: dict, reftime: datetime, stamp: str) -> None:
        pass

    def check_history(self, conn):
        """
        create fire_crawl_history table if not exist
        """
        cur = conn.cursor()
        # if table not exist
        cur.execute(self.sql_check_if_history_table_exists)
        tables = cur.fetchall()
        if len(tables) == 0:
            cur.execute(FireDumper.sql_create_history_table)
            conn.commit()
        cur.close()


    def retrieve_all_fires(self):
        """
        retrieve all fires in the database
        :return: set
        """
        with Connection() as connect:
            self.check_history(connect)
            cur = connect.cursor()
            cur.execute(self.sql_retrieve_all_fires)
            result = cur.fetchall()
        return result


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
    sql_create_history_table = 'CREATE TABLE IF NOT EXISTS fire_crawl_history (fireyear int4, firename VARCHAR (20), PRIMARY KEY (fireyear, firename))'
    sql_retrieve_all_fires = 'SELECT * FROM fire_crawl_history'
    sql_check_if_fire_info_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_info\''
    sql_create_fire_info_table = 'CREATE TABLE IF NOT EXISTS fire_info (firename VARCHAR (20), fire_if_sequence boolean, fireagency VARCHAR (20), firetime timestamp, firegeom polygon, PRIMARY KEY (firename, firetime))'
    sql_insert_fire_into_history = 'INSERT INTO "fire_crawl_history" (fireyear, firename) VALUES (%(year)s, %(firename)s) ON CONFLICT DO NOTHING'
    sql_insert_fire_into_info = 'INSERT INTO "fire_info" (firename, fire_if_sequence, fireagency, firetime, firegeom) VALUES (%(firename)s,%(if_sequence)s,%(agency)s,%(datetime)s,%(geopolygon)s) ON CONFLICT DO NOTHING'
    sql_count_records = 'SELECT COUNT(*) FROM fire_crawl_history'

    def __init__(self):
        super().__init__()

    def insert(self) -> None:
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

    def check_info(self, conn):
        """
        create fire_crawl_history table if not exist
        """
        cur = conn.cursor()
        # if table not exist
        cur.execute(self.sql_check_if_fire_info_table_exists)
        tables = cur.fetchall()
        if len(tables) == 0:
            cur.execute(FireDumper.sql_create_fire_info_table)
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

    def insert(self, info: dict):
        s = "("
        for t in info["geopolygon"]:
            s += "({},{}),".format(t[0], t[1])
        info["geopolygon"] = s[:-1] + ")"
        with Connection() as connect:
            self.check_info(connect)
            cur = connect.cursor()
            cur.execute(self.sql_insert_fire_into_history, info)
            cur.execute(self.sql_insert_fire_into_info, info)
            connect.commit()
            cur.execute(self.sql_count_records)
            self.inserted_count = cur.fetchone()[0]
            cur.close()


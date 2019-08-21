from typing import List, Dict
import logging
import rootpath
rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')

class FireDumper(DumperBase):
    """
    Table 1(fire_crawl_history): fireyear state firename
    Table 2(fire_geoms): firename firetime firegeom
    """
    # code for checking
    sql_check_if_fire_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire\''

    sql_check_if_history_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_history\''

    sql_check_if_fire_merged_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_merged\''

    # code for creating
    sql_create_history_table = 'CREATE TABLE IF NOT EXISTS fire_history (id integer, year int4, state VARCHAR(40), ' \
                                   'name VARCHAR (40), url text, PRIMARY KEY (id))'

    sql_create_fire_merged_table = 'CREATE TABLE IF NOT EXISTS fire_merged (name VARCHAR (40), if_sequence boolean, ' \
                                       'agency VARCHAR (80), state VARCHAR(15), id INTEGER , start_time timestamp, ' \
                                       'end_time timestamp, geom_full geometry, geom_1e4 geometry, geom_1e3 geometry, ' \
                                       'geom_1e2 geometry,geom_center geometry, max_area float, PRIMARY KEY (id))'

    sql_create_fire_table = 'CREATE TABLE IF NOT EXISTS fire (name VARCHAR (40), if_sequence boolean, agency ' \
                                 'VARCHAR (20), state VARCHAR(15), id INTEGER , time timestamp, geom_full geometry, ' \
                                 'geom_1e4 geometry, geom_1e3 geometry, geom_1e2 geometry, geom_center geometry, area float, ' \
                                 'PRIMARY KEY (name, time))'
    # code for updating
    sql_insert_fire_history = 'INSERT INTO fire_history (id, year, state, name,url) VALUES (%(id)s,%(year)s,' \
                                   '%(state)s, %(firename)s, %(url)s) ON CONFLICT DO NOTHING'

    sql_insert_fire = 'INSERT INTO fire (name, if_sequence, agency, state, id, time, geom_full, geom_1e4, ' \
                                'geom_1e3, geom_1e2, geom_center, area) VALUES (%(firename)s,%(if_sequence)s,%(agency)s,' \
                                '%(state)s,%(id)s,%(datetime)s,%(geopolygon_full)s,%(geopolygon_large)s,' \
                                '%(geopolygon_medium)s,%(geopolygon_small)s, ' \
                                'st_astext(st_centroid(st_geomfromtext(%(geopolygon_small)s))), %(area)s) ON CONFLICT DO NOTHING'


    sql_insert_fire_into_merged = 'INSERT INTO fire_merged(name, if_sequence, agency, state, id, start_time, end_time, ' \
                                  'geom_full, geom_1e4, geom_1e3, geom_1e2, geom_center, max_area)' \
                                  'Values (%s, %s, %s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET ' \
                                  'if_sequence = true, agency = excluded.agency, end_time = excluded.end_time, ' \
                                  'geom_full = excluded.geom_full,geom_1e4 = Excluded.geom_1e4,geom_1e3 = Excluded.geom_1e3,' \
                                  'geom_1e2 = Excluded.geom_1e2, geom_center = EXCLUDED.geom_center,max_area=EXCLUDED.max_area'

    sql_update_fire_info = 'UPDATE fire SET id = %(id)s WHERE name = %(name)s AND time >= %(end_time)s::timestamp AND ' \
                           'time <= %(start_time)s::timestamp;'

    # code for accessing
    sql_retrieve_all_fires = 'SELECT year,state,name FROM fire_history'
    sql_count_records = 'SELECT COUNT(*) FROM fire'
    sql_get_lastest_id = 'SELECT MAX(id) FROM fire_history'
    sql_get_latest_fire = 'SELECT a.id,h.year, h.state, h.name ' \
                          'from (SELECT id FROM fire_merged Where abs(DATE_PART(\'day\', ' \
                          'end_time - now())) < 10) a, fire_history h where h.id = a.id;'
    sql_get_latest_aggregation = 'SELECT f.name, f.if_sequence,string_agg(distinct (f.agency), \', \'),f.state,f.id,' \
                                 'min(f.time),Max(f.time), st_astext(st_union(st_makevalid(f.geom_full))) as geom_full,' \
                                 'st_astext(st_union(st_makevalid(f.geom_1e4))),st_astext(st_union(st_makevalid(f.geom_1e3))),' \
                                 'st_astext(st_union(st_makevalid(f.geom_1e2))),st_astext(st_centroid(st_union(st_makevalid(f.geom_center)))), ' \
                                 'max(f.area) FROM (SELECT * FROM fire where id = {}) f Group by f.name, f.if_sequence, f.state, f.id'

    def __init__(self):
        super().__init__()

    def check_history(self, conn):
        """
        create fire_crawl_history table if not exist
        """
        cur = conn.cursor()
        # if table not exist
        cur.execute(self.sql_check_if_history_table_exists)
        tables = cur.fetchall()
        if len(tables) == 0:
            logger.info("No history table exists. Creating a new one.")
            cur.execute(FireDumper.sql_create_history_table)
            conn.commit()
        logger.info("History table created.")
        cur.close()

    def check_info(self, conn):
        """
        create fire_info table if not exist
        """
        cur = conn.cursor()
        # if table not exist
        cur.execute(self.sql_check_if_fire_table_exists)
        tables = cur.fetchall()
        if len(tables) == 0:
            logger.info("No fire table exists. Creating a new one.")
            cur.execute(FireDumper.sql_create_fire_table)
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
        with Connection() as connect:
            self.check_info(connect)
            cur = connect.cursor()
            cur.execute(self.sql_insert_fire, info)
            connect.commit()
            cur.execute(self.sql_count_records)
            self.inserted_count = cur.fetchone()[0]
            cur.close()
        logger.info(f"Finished inserting file: {info['firename']}{info['datetime']}")
        logger.info(f"record count:{self.inserted_count}")

    def insert_history(self,year,name,state,id, current_year):
        with Connection() as connect:
            urlyear = ""
            if year == current_year:
                urlyear = 'current_year'
            else:
                urlyear = str(year)
            info = {"year":year,"firename":name, "state":state, "id":id, "url":f"https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/{urlyear}_fire_data/{state}/{name}/"}
            cur = connect.cursor()
            cur.execute(self.sql_insert_fire_history, info)
            connect.commit()
            cur.close

    def get_latest_fire_id(self):
        with Connection() as connect:
            cur = connect.cursor()
            cur.execute(self.sql_get_lastest_id)
            result = cur.fetchone()[0]
        return result

    def get_recent_records(self):
        """
        return the list of ids of most recent records
        :return:
        """
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute(self.sql_check_if_fire_merged_table_exists)
            tables = cur.fetchall()
            if len(tables) == 0:
                logger.info("No aggregated table exists. Creating a new one.")
                cur.execute(FireDumper.sql_create_fire_merged_table)
                conn.commit()
            cur.execute(self.sql_get_latest_fire)
            result = cur.fetchall()
        return result

    # def check_if_aggregation_exist(self, id):
    #     """
    #     check if the record with an id exist in aggregation table
    #     if yes then delete it
    #     :param id:
    #     :return:
    #     """
    #     with Connection() as conn:
    #         cur = conn.cursor()
    #         cur.execute(f"SELECT * FROM fire_merged f WHERE f.id = {id}")
    #         table = cur.fetchall()
    #         if len(table) != 0:
    #             logger.info("Record exists, deleting")
    #             cur.execute(f'DELETE from fire_merged where id = {id}')
    #             conn.commit()
    #             logger.info("deleted")


    def after_inserting_into_fire_info(self, id:int,year,name,state,current_year):
        """
        Procedure to be execute after inserting a set of fire into fire_info
        :param id: int
        :return:
        """
        with Connection() as conn:
            cur = conn.cursor()
            # check if fire_aggregate table exist
            cur.execute(self.sql_check_if_fire_merged_table_exists)
            tables = cur.fetchall()
            if len(tables) == 0:
                logger.info("No aggregated table exists. Creating a new one.")
                cur.execute(FireDumper.sql_create_fire_merged_table)
                conn.commit()
            cur.execute(self.sql_get_latest_aggregation.format(id))
            aggregated_with_id = cur.fetchall()
            if aggregated_with_id == []:
                self.insert_history(year,name,state,id,current_year)
                return id
            new_id = id
            for i in range(len(aggregated_with_id)):
                new_id = new_id + i
                info = {"name":aggregated_with_id[i][0],
                        "if_sequence": aggregated_with_id[i][1],
                        "agency": aggregated_with_id[i][2],
                        "state": aggregated_with_id[i][3],
                        "id": new_id,
                        "start_time": aggregated_with_id[i][5],
                        "end_time": aggregated_with_id[i][6],
                        "geom_full": aggregated_with_id[i][7],
                        "geom_1e4": aggregated_with_id[i][8],
                        "geom_1e3": aggregated_with_id[i][9],
                        "geom_1e2": aggregated_with_id[i][10],
                        "geom_center": aggregated_with_id[i][11],
                        "max_area": aggregated_with_id[i][12]
                        }
                info_tuple = [ i for i  in info.values()]
                # update their id in fire_info
                cur.execute(self.sql_update_fire_info, info)
                # insert this set in fire_aggregate
                cur.execute(self.sql_insert_fire_into_merged,info_tuple)

                conn.commit()
                # insert this set into fire_crawl_history
                self.insert_history(year,name,state,id,current_year)
        return new_id


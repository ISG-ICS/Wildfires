from typing import List, Dict

import rootpath
rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection

class FireDumper(DumperBase):
    """
    Table 1(fire_crawl_history): fireyear state firename
    Table 2(fire_geoms): firename firetime firegeom
    """
    # code for checking
    sql_check_if_history_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_crawl_history\''
    sql_check_if_fire_info_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_info\''
    sql_check_if_fire_aggregated_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_aggregated\''

    # code for creating
    sql_create_history_table = 'CREATE TABLE IF NOT EXISTS fire_crawl_history (id integer, year int4, state VARCHAR(40), ' \
                               'name VARCHAR (40), url text, PRIMARY KEY (id))'
    sql_create_fire_info_table = 'CREATE TABLE IF NOT EXISTS fire_info (name VARCHAR (40), if_sequence boolean, agency ' \
                                 'VARCHAR (20), state VARCHAR(15), id INTEGER , time timestamp, geom_full geometry, ' \
                                 'geom_1e4 geometry, geom_1e3 geometry, geom_1e2 geometry, geom_center geometry, ' \
                                 'PRIMARY KEY (name, time))'
    sql_create_fire_aggregated_table = 'CREATE TABLE IF NOT EXISTS fire_aggregated (name VARCHAR (40), if_sequence boolean, ' \
                                       'agency VARCHAR (80), state VARCHAR(15), id INTEGER , starttime timestamp, ' \
                                       'endtime timestamp, geom_full geometry, geom_1e4 geometry, geom_1e3 geometry, ' \
                                       'geom_1e2 geometry,geom_center geometry, PRIMARY KEY (id))'

    # code for updating
    sql_insert_fire_into_history = 'INSERT INTO fire_crawl_history (id, year, state, name,url) VALUES (%(id)s,%(year)s,' \
                                   '%(state)s, %(firename)s, %(url)s) ON CONFLICT DO NOTHING'
    sql_insert_fire_into_info = 'INSERT INTO fire_info (name, if_sequence, agency, state, id, time, geom_full, geom_1e4, ' \
                                'geom_1e3, geom_1e2, geom_center) VALUES (%(firename)s,%(if_sequence)s,%(agency)s,' \
                                '%(state)s,%(id)s,%(datetime)s,%(geopolygon_full)s,%(geopolygon_large)s,' \
                                '%(geopolygon_medium)s,%(geopolygon_small)s, ' \
                                'st_astext(st_centroid(st_geomfromtext(%(geopolygon_small)s)))) ON CONFLICT DO NOTHING'
    sql_insert_fire_into_aggregated = 'INSERT INTO fire_aggregated(name, if_sequence, agency, state, id, starttime, ' \
                                      'endtime, geom_full, geom_1e4, geom_1e3, geom_1e2, geom_center) ' \
                                      'SELECT f.name, f.if_sequence,string_agg(distinct (f.agency), \', \'),f.state,' \
                                      'f.id,min(f.time),Max(f.time), st_astext(st_union(st_makevalid(f.geom_full))) ' \
                                      'as geom_full,st_astext(st_union(st_makevalid(f.geom_1e4))),' \
                                      'st_astext(st_union(st_makevalid(f.geom_1e3))),' \
                                      'st_astext(st_union(st_makevalid(f.geom_1e2))),' \
                                      'st_astext(st_centroid(st_union(f.geom_center))) ' \
                                      'FROM (SELECT * FROM fire_info where id = %(id)s) f Group by ' \
                                      'f.name, f.if_sequence, f.state, f.id'
    sql_insert_fire_into_aggregated_single = 'INSERT INTO fire_aggregated(name, if_sequence, agency, state, id, starttime, endtime, geom_full, geom_1e4, geom_1e3, geom_1e2, geom_center) ' \
                                             'VALUES (%(name)s, %(if_sequence)s, %(agency)s, %(state)s,%(id)s, %(starttime)s, %(endtime)s, %(geom_full)s, %(geom_1e4)s, %(geom_1e3)s, %(geom_1e2)s,%(geom_center)s) ON CONFLICT DO NOTHING'
    sql_update_fire_info = 'UPDATE fire_info SET id = %(id)s WHERE name = %(name)s AND time >= %(endtime)s::timestamp AND time <= %(starttime)s::timestamp;'

    # code for accessing
    sql_retrieve_all_fires = 'SELECT year,state,name FROM fire_crawl_history'
    sql_count_records = 'SELECT COUNT(*) FROM fire_info'
    sql_get_lastest_id = 'SELECT MAX(id) FROM fire_crawl_history'
    sql_get_latest_fire = 'SELECT a.id, h.year, h.state, h.name ' \
                          'from (SELECT id FROM fire_aggregated Where abs(DATE_PART(\'day\', ' \
                          'endtime - now())) < 10) a, fire_crawl_history h where h.id = a.id;'
    sql_get_latest_aggregation = 'SELECT f.name, f.if_sequence,string_agg(distinct (f.agency), \', \'),f.state,f.id,min(f.time),Max(f.time), st_astext(st_union(st_makevalid(f.geom_full))) as geom_full,st_astext(st_union(st_makevalid(f.geom_1e4))),st_astext(st_union(st_makevalid(f.geom_1e3))),st_astext(st_union(st_makevalid(f.geom_1e2))),st_astext(st_centroid(st_union(f.geom_center))) FROM (SELECT * FROM fire_info where id = {}) f Group by f.name, f.if_sequence, f.state, f.id'

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
            print("No history table exists. Creating a new one.")
            cur.execute(FireDumper.sql_create_history_table)
            conn.commit()
        cur.close()

    def check_info(self, conn):
        """
        create fire_info table if not exist
        """
        cur = conn.cursor()
        # if table not exist
        cur.execute(self.sql_check_if_fire_info_table_exists)
        tables = cur.fetchall()
        if len(tables) == 0:
            print("No info table exists. Creating a new one.")
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
        print("Inserting fire:",info["firename"],info["datetime"])
        with Connection() as connect:
            self.check_info(connect)
            cur = connect.cursor()
            cur.execute(self.sql_insert_fire_into_info, info)
            connect.commit()
            cur.execute(self.sql_count_records)
            self.inserted_count = cur.fetchone()[0]
            cur.close()
        print("Finished inserting file:",info["firename"],info["datetime"])
        print("record count:",self.inserted_count)

    def insert_history(self,year,name,state,id, current_year):
        with Connection() as connect:
            urlyear = ""
            if year == current_year:
                urlyear = 'current_year'
            else:
                urlyear = str(year)
            info = {"year":year,"firename":name, "state":state, "id":id, "url":f"https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/{urlyear}_fire_data/{state}/{name}/"}
            cur = connect.cursor()
            cur.execute(self.sql_insert_fire_into_history, info)
            connect.commit()
            cur.close



    def get_latest_fire_id(self):
        with Connection() as connect:
            cur = connect.cursor()
            cur.execute(self.sql_get_lastest_id)
            result = cur.fetchone()[0]
            # print(result)
            # print(type(result))
        return result

    def aggregate(self, id):
        with Connection() as conn:
            cur = conn.cursor()
            self.check_aggregated(conn)
            info = {"id": id}
            cur.execute(self.sql_get_latest_aggregation,info)
            result = cur.fetchall()
            if len(result) > 1:
                for record in result:
                    print(record)
                    cur.execute(self.sql_insert_fire_into_aggregated_single, record)
                    cur.execute()
                    id += 1

            cur.execute(self.sql_insert_fire_into_aggregated,info)
            conn.commit()
        return

    def get_recent_records(self):
        """
        return the list of ids of most recent records
        :return:
        """
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute(self.sql_check_if_fire_aggregated_table_exists)
            tables = cur.fetchall()
            if len(tables) == 0:
                print("No aggregated table exists. Creating a new one.")
                cur.execute(FireDumper.sql_create_fire_aggregated_table)
                conn.commit()
            cur.execute(self.sql_get_latest_fire)
            result = cur.fetchall()
        return result

    def check_if_aggregation_exist(self, id):
        """
        check if the record with an id exist in aggregation table
        if yes then delete it
        :param id:
        :return:
        """
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM fire_aggregated f WHERE f.id = {id}")
            table = cur.fetchall()
            if len(table) != 0:
                print("Record exists, deleting")
                cur.execute(f'DELETE from fire_aggregated where id = {id}')
                conn.commit()
                print("deleted")


    def after_inserting_into_fire_info(self, id:int,year,name,state,current_year):
        """
        Procedure to be execute after inserting a set of fire into fire_info
        :param id: int
        :return:
        """
        with Connection() as conn:
            cur = conn.cursor()
            # check if fire_aggregate table exist
            cur.execute(self.sql_check_if_fire_aggregated_table_exists)
            tables = cur.fetchall()
            if len(tables) == 0:
                print("No aggregated table exists. Creating a new one.")
                cur.execute(FireDumper.sql_create_fire_aggregated_table)
                conn.commit()
            cur.execute(self.sql_get_latest_aggregation.format(id))
            aggregated_with_id = cur.fetchall()
            print(aggregated_with_id)
            new_id = id
            for i in range(len(aggregated_with_id)):
                new_id = new_id + i
                info = {"name":aggregated_with_id[i][0],
                        "if_sequence": aggregated_with_id[i][1],
                        "agency": aggregated_with_id[i][2],
                        "state": aggregated_with_id[i][3],
                        "id": new_id,
                        "starttime": aggregated_with_id[i][5],
                        "endtime": aggregated_with_id[i][6],
                        "geom_full": aggregated_with_id[i][7],
                        "geom_1e4": aggregated_with_id[i][8],
                        "geom_1e3": aggregated_with_id[i][9],
                        "geom_1e2": aggregated_with_id[i][10],
                        "geom_center": aggregated_with_id[i][11]
                        }
                # update their id in fire_info
                cur.execute(self.sql_update_fire_info, info)
                # insert this set in fire_aggregate
                cur.execute(self.sql_insert_fire_into_aggregated_single,info)
                conn.commit()
                # insert this set into fire_crawl_history
                self.insert_history(year,name,state,id,current_year)
        return new_id


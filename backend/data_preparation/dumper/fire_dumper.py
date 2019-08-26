from typing import List, Dict
import logging
import rootpath
rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')

class FireDumper(DumperBase):
    """
    Fire Dumper class
    In this function, there are mainly operations on 3 tables:
    fire: schema: name, if_sequence, agency, state,id, time, geom_full, geom_1e4,geom_1e3, geom_1e2,geom_center, area.
          primary key: (name, time)
    (records in fire is only smaller fire event records that represent a single fire polygon record at a certain moment)
    fire_history: schema: id, year, state, name, url.
          primary key: id
    (records in fire_history is a fire that takes a whole webpage on rmgsc, so 'name' here is the urlname)
    fire_merged: schema: name, if_sequence, agency, state, id,start_time, end_time, geom_full, geom_1e4, geom_1e3,
    geom_center, max_area
          primary key: id
    (records in fire_merged is a fire that takes a whole webpage on rmgsc, start_time is from the first fire record and
    end_time is from the last fire record)
    """

    # code for checking if a database exists
    sql_check_if_fire_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire\''
    # sql_check_if_fire_table_exists: check if "fire" table exists
    sql_check_if_history_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_history\''
    # sql_check_if_history_table_exists: check if "fire_history" table exists
    sql_check_if_fire_merged_table_exists = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_merged\''
    # sql_check_if_fire_merged_table_exists: check if "fire_merged" table exists

    # code for creating a table if it doesn't exist
    sql_create_history_table = 'CREATE TABLE IF NOT EXISTS fire_history (id integer, year int4, state VARCHAR(40), ' \
                                   'name VARCHAR (40), url text, PRIMARY KEY (id))'
    # sql_create_history_table: create fire_history table if it doesn't exist
    sql_create_fire_merged_table = 'CREATE TABLE IF NOT EXISTS fire_merged (name VARCHAR (40), if_sequence boolean, ' \
                                       'agency VARCHAR (80), state VARCHAR(15), id INTEGER , start_time timestamp, ' \
                                       'end_time timestamp, geom_full geometry, geom_1e4 geometry, geom_1e3 geometry, ' \
                                       'geom_1e2 geometry,geom_center geometry, max_area float, PRIMARY KEY (id))'
    # sql_create_fire_merged_table: create fire_merged table if it doesn't exist
    sql_create_fire_table = 'CREATE TABLE IF NOT EXISTS fire (name VARCHAR (40), if_sequence boolean, agency ' \
                                 'VARCHAR (20), state VARCHAR(15), id INTEGER , time timestamp, geom_full geometry, ' \
                                 'geom_1e4 geometry, geom_1e3 geometry, geom_1e2 geometry, geom_center geometry, area float, ' \
                                 'PRIMARY KEY (name, time))'
    # sql_create_fire_table: create fire table if it doesn't exist'

    # code for updating records or inserting new records
    sql_insert_fire_history = 'INSERT INTO fire_history (id, year, state, name,url) VALUES (%(id)s,%(year)s,' \
                                   '%(state)s, %(firename)s, %(url)s) ON CONFLICT DO NOTHING'
    # sql_insert_fire_history: insert a new fire record into fire_history
    sql_insert_fire = 'INSERT INTO fire (name, if_sequence, agency, state, id, time, geom_full, geom_1e4, ' \
                                'geom_1e3, geom_1e2, geom_center, area) VALUES (%(firename)s,%(if_sequence)s,%(agency)s,' \
                                '%(state)s,%(id)s,%(datetime)s,%(geopolygon_full)s,%(geopolygon_large)s,' \
                                '%(geopolygon_medium)s,%(geopolygon_small)s, ' \
                                'st_astext(st_centroid(st_geomfromtext(%(geopolygon_small)s))), %(area)s) ON CONFLICT DO NOTHING'
    # sql_insert_fire: insert a new fire record into fire
    sql_insert_fire_into_merged = 'INSERT INTO fire_merged(name, if_sequence, agency, state, id, start_time, end_time, ' \
                                  'geom_full, geom_1e4, geom_1e3, geom_1e2, geom_center, max_area)' \
                                  'Values (%s, %s, %s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET ' \
                                  'if_sequence = true, agency = excluded.agency, end_time = excluded.end_time, ' \
                                  'geom_full = excluded.geom_full,geom_1e4 = Excluded.geom_1e4,geom_1e3 = Excluded.geom_1e3,' \
                                  'geom_1e2 = Excluded.geom_1e2, geom_center = EXCLUDED.geom_center,max_area=EXCLUDED.max_area'
    # sql_insert_fire_into_merged: insert a new fire record into fire_merged
    sql_update_fire_info = 'UPDATE fire SET id = %(id)s WHERE name = %(name)s AND time >= %(start_time)s::timestamp AND ' \
                           'time <= %(end_time)s::timestamp;'
    # update fire info when: there are one fire in temp folder but records are from fireEvents with different name, one
    # record will be seperated into two records
    # so id in fire table need to be updated with a larger number

    # code for requesting fire information
    # retrieve all fire information
    sql_retrieve_all_fires = 'SELECT year,state,name FROM fire_history'
    # retrieve the count of records from fire
    sql_count_records = 'SELECT COUNT(*) FROM fire'
    # get the last id from fire_history table
    sql_get_lastest_id = 'SELECT MAX(id) FROM fire_history'
    # get the recent fire whose last record is within 10 days of the current date
    sql_get_latest_fire = 'SELECT a.id,h.year, h.state, h.name ' \
                          'from (SELECT id FROM fire_merged Where abs(DATE_PART(\'day\', ' \
                          'end_time - now())) < 10) a, fire_history h where h.id = a.id;'
    # return the aggregated fire information with a given id
    sql_get_latest_aggregation = 'SELECT f.name, f.if_sequence,string_agg(distinct (f.agency), \', \'),f.state,f.id,' \
                                 'min(f.time),Max(f.time), st_astext(st_union(st_makevalid(f.geom_full))) as geom_full,' \
                                 'st_astext(st_union(st_makevalid(f.geom_1e4))),st_astext(st_union(st_makevalid(f.geom_1e3))),' \
                                 'st_astext(st_union(st_makevalid(f.geom_1e2))),st_astext(st_centroid(st_union(st_makevalid(f.geom_center)))), ' \
                                 'max(f.area) FROM (SELECT * FROM fire where id = {}) f Group by f.name, f.if_sequence, f.state, f.id'

    def __init__(self):
        """
        Initialize the dumper object
        """
        super().__init__()

    def check_history(self, conn):
        """
        Check if the fire_history table exists,
        Create fire_crawl_history table if not exist
        :param conn: connection
        """
        # create a cursor
        cur = conn.cursor()
        # check if the fire_history table exists
        # if the pipeline is run for the first time
        # then the fire_history table will not exist
        cur.execute(self.sql_check_if_history_table_exists)
        tables = cur.fetchall()
        # table is the result of the statement: sql_check_if_history_table_exists
        if len(tables) == 0:
            # if table is empty, which means the fire_history table does not exists
            logger.info("No history table exists. Creating a new one.")
            cur.execute(FireDumper.sql_create_history_table)
            # create the fire_history table
            conn.commit()
            # commit the transaction so the change will be saved
            logger.info("History table created.")
        else:
            logger.info("Find the fire_history table, continue >..")
        cur.close()

    def check_info(self, conn):
        """
        Check if the fire table exists
        Create fire table if not exist
        :param conn:connection
        """
        # create a cursor
        cur = conn.cursor()
        # check if the fire_history table exists
        # if the pipeline is run for the first time
        # then the fire_history table will not exist
        cur.execute(self.sql_check_if_fire_table_exists)
        tables = cur.fetchall()
        # table is the result of the statement: sql_check_if_history_table_exists
        if len(tables) == 0:
            # if table is empty, which means the fire_history table does not exists
            logger.info("No fire table exists. Creating a new one.")
            cur.execute(FireDumper.sql_create_fire_table)
            # create the fire_history table
            conn.commit()
            # commit the transaction so the change will be saved
            logger.info("Fire table created.")
        else:
            logger.info("Find the fire table, continue >..")
        cur.close()


    def retrieve_all_fires(self):
        """
        Retrieve all fires in the database
        :return: set of tuples
        """
        with Connection() as connect:
            # check if the fire_history table exists
            # if not exist, executing sql_retrieve_all_fires will return an error
            self.check_history(connect)
            cur = connect.cursor()
            # retrieve all fires in fire_history
            cur.execute(self.sql_retrieve_all_fires)
            result = cur.fetchall()
            # result now is a set of tuples: (year, state, urlname)
            # e.g. for https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2015_fire_data/California/Deer_Horn_2/
            # the history tuple is : (2015, California, Deer_Horn_2)
        return result

    def insert(self, info: dict):
        """
        Insert a single fire record into fire table.
        :param info:dict to insert, from extractor.extract()
        :return:None
        """
        with Connection() as connect:
            # check if the fire table exists
            # if not exist, executing sql_insert will cause an error
            self.check_info(connect)
            # create cursor
            cur = connect.cursor()
            # execute insert statement
            cur.execute(self.sql_insert_fire, info)
            connect.commit()
            # commit transaction
            cur.execute(self.sql_count_records)
            # count number of records
            self.inserted_count = cur.fetchone()[0]
            cur.close()
        # print logging message for debugging
        logger.info(f"Finished inserting file: {info['firename']}{info['datetime']}")
        logger.info(f"record count:{self.inserted_count}")

    def insert_history(self,year,name,state,id, current_year):
        """
        Insert a fire record into fire_history table
        :param year: year of fire from url
        :param name: url name of fire
        :param state: state of fire from url
        :param id: id of fire, from the counter from data_from_fire
        :param current_year: current year, from datetime
        :return: None
        """
        with Connection() as connect:
            if year == current_year:
                # if year == current_year, then the fire's url year part is current_year_fire_data
                urlyear = 'current_year'
            else:
                # if year != current_year, then the fire's url year part is the year as a string
                urlyear = str(year)
            # make the dictionary to be inserted into fire_history
            info = {"year": year,
                    "firename": name,
                    "state": state,
                    "id": id,
                    "url": f"https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/{urlyear}_fire_data/{state}/{name}/"}
            # create the cursor
            cur = connect.cursor()
            # execute insert statement
            cur.execute(self.sql_insert_fire_history, info)
            # commit transaction
            connect.commit()
            # close connection
            cur.close()

    def get_latest_fire_id(self):
        """
        Get the latest fire id to pass to the counter in data_from_fire
        :return: int
        """
        with Connection() as connect:
            # create cursor
            cur = connect.cursor()
            # execute select statement
            cur.execute(self.sql_get_lastest_id)
            # the latest fire id is the first and only entry of the result
            result = cur.fetchone()[0]
        return result

    def get_recent_records(self):
        """
        Return the list of ids of most recent records
        :return:
        """
        with Connection() as conn:
            # create cursor
            cur = conn.cursor()
            # execute select statement to see if  fire_merged table exists
            cur.execute(self.sql_check_if_fire_merged_table_exists)
            tables = cur.fetchall()
            # if it doesn't exist, create one
            if len(tables) == 0:
                logger.info("No aggregated table exists. Creating a new one.")
                cur.execute(FireDumper.sql_create_fire_merged_table)
                conn.commit()
            # execute select statement, get the fire ids of those fire whose end_date is within 10 days
            # these are fires that might update these days
            cur.execute(self.sql_get_latest_fire)
            result = cur.fetchall()
            # result is a list of tuples (id, year, state, urlname)
        return result

    def after_inserting_into_fire_info(self, id:int,year,name,state,current_year):
        '''
         A sequence of operations after inserting all records of a fire into fire table
         including insertion into fire_merged, fire_history
        :param id: int, id of the fire
        :param year:int
        :param name:str
        :param state:str
        :param current_year:int
        :return:
        '''
        with Connection() as conn:
            # create cursor
            cur = conn.cursor()
            # check if fire_merged table exists
            cur.execute(self.sql_check_if_fire_merged_table_exists)
            tables = cur.fetchall()
            if len(tables) == 0:
                # if fire_merged table does not exist, create a new one
                # this can happen if this is the first time running
                logger.info("No aggregated table exists. Creating a new one.")
                cur.execute(FireDumper.sql_create_fire_merged_table)
                conn.commit()
                # commit transaction
            # get the aggregated record of the last fire inserted into fire table
            cur.execute(self.sql_get_latest_aggregation.format(id))
            aggregated_with_id = cur.fetchall()
            # aggregated_with_id is now the aggregated record of last fire inserted into fire table
            if len(aggregated_with_id) == 0:
                # if this id is an empty record, then there is no aggregated fire records
                # in this situation, we only mark the url as crawled, by inserting it into fire_history
                self.insert_history(year, name, state, id, current_year)
                # return the latest fire id
                return id
            # set a temporary value new_id as id
            new_id = id
            # the records can be dirty. Sometimes the folder of one fire includes fire with a different name
            # then when merged, the return list has more than one records
            # so a for loop is needed to deal with this situation
            for i in range(len(aggregated_with_id)):
                new_id = new_id + i
                # Most situation, there is only one record, new_id = id
                # if there is more than one, new_id will be id + i
                # create the dictionary for all values in aggregated record
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
                # transform the dictionary into a tuple for easier handling
                info_tuple = [i for i in info.values()]
                # update their id in fire_info
                # here, if the new_id is diffrent from id, the fire with that name will be updated with the new id
                cur.execute(self.sql_update_fire_info, info)
                # insert this set in fire_aggregate
                cur.execute(self.sql_insert_fire_into_merged, info_tuple)
                # commit the transaction
                conn.commit()
                # insert this set into fire_crawl_history, mark it as crawled
                self.insert_history(year, name, state, id, current_year)
        return new_id


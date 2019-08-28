"""
@author: Scarlett Zhang
This file has 2 classes:
InvalidRecordError
FireDumper
"""
from typing import List, Dict, Tuple
import logging
import rootpath
rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection
from typing import Set
logger = logging.getLogger('TaskManager')


class InvalidRecordError(Exception):
    pass


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
    SQL_CHECK_IF_FIRE_TABLE_EXISTS = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire\''
    # SQL_CHECK_IF_FIRE_TABLE_EXISTS: check if "fire" table exists
    SQL_CHECK_IF_HISTORY_TABLE_EXISTS = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_history\''
    # SQL_CHECK_IF_HISTORY_TABLE_EXISTS: check if "fire_history" table exists
    SQL_CHECK_IF_FIRE_MERGED_TABLE_EXISTS = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'fire_merged\''
    # SQL_CHECK_IF_FIRE_MERGED_TABLE_EXISTS: check if "fire_merged" table exists

    # code for creating a table if it doesn't exist
    SQL_CREATE_HISTORY_TABLE = 'CREATE TABLE IF NOT EXISTS fire_history (id integer, year int4, state VARCHAR(40), ' \
                                   'name VARCHAR (40), url text, PRIMARY KEY (id))'
    # SQL_CREATE_HISTORY_TABLE: create fire_history table if it doesn't exist
    SQL_CREATE_FIRE_MERGED_TABLE = 'CREATE TABLE IF NOT EXISTS fire_merged (name VARCHAR (40), if_sequence boolean, ' \
                                       'agency VARCHAR (80), state VARCHAR(15), id INTEGER , start_time timestamp, ' \
                                       'end_time timestamp, geom_full geometry, geom_1e4 geometry, geom_1e3 geometry, ' \
                                       'geom_1e2 geometry,geom_center geometry, max_area float, PRIMARY KEY (id))'
    # SQL_CREATE_FIRE_MERGED_TABLE: create fire_merged table if it doesn't exist
    SQL_CREATE_FIRE_TABLE = 'CREATE TABLE IF NOT EXISTS fire (name VARCHAR (40), if_sequence boolean, agency ' \
                                 'VARCHAR (20), state VARCHAR(15), id INTEGER , time timestamp, geom_full geometry, ' \
                                 'geom_1e4 geometry, geom_1e3 geometry, geom_1e2 geometry, geom_center geometry, area float, ' \
                                 'PRIMARY KEY (name, time))'
    # SQL_CREATE_FIRE_TABLE: create fire table if it doesn't exist'

    # code for updating records or inserting new records
    # "%(id)s": when this statement is executed with cur.execute(), the second parameter is a dictionary with has "id"
    # as the key and the value of id as the value
    SQL_INSERT_FIRE_HISTORY = 'INSERT INTO fire_history (id, year, state, name,url) VALUES (%(id)s,%(year)s,' \
                                   '%(state)s, %(firename)s, %(url)s) ON CONFLICT DO NOTHING'
    # SQL_INSERT_FIRE_HISTORY: insert a new fire record into fire_history
    SQL_INSERT_FIRE = 'INSERT INTO fire (name, if_sequence, agency, state, id, time, geom_full, geom_1e4, ' \
                                'geom_1e3, geom_1e2, geom_center, area) VALUES (%(firename)s,%(if_sequence)s,%(agency)s,' \
                                '%(state)s,%(id)s,%(datetime)s,%(geopolygon_full)s,%(geopolygon_large)s,' \
                                '%(geopolygon_medium)s,%(geopolygon_small)s, ' \
                                'st_astext(st_centroid(st_geomfromtext(%(geopolygon_small)s))), %(area)s) ON CONFLICT DO NOTHING'
    # SQL_INSERT_FIRE: insert a new fire record into fire
    SQL_INSERT_FIRE_INTO_MERGED = 'INSERT INTO fire_merged(name, if_sequence, agency, state, id, start_time, end_time, ' \
                                  'geom_full, geom_1e4, geom_1e3, geom_1e2, geom_center, max_area)' \
                                  'Values (%s, %s, %s,%s, %s, %s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO UPDATE SET ' \
                                  'if_sequence = true, agency = excluded.agency, end_time = excluded.end_time, ' \
                                  'geom_full = excluded.geom_full,geom_1e4 = Excluded.geom_1e4,geom_1e3 = Excluded.geom_1e3,' \
                                  'geom_1e2 = Excluded.geom_1e2, geom_center = EXCLUDED.geom_center,max_area=EXCLUDED.max_area'
    # SQL_INSERT_FIRE_INTO_MERGED: insert a new fire record into fire_merged
    SQL_UPDATE_FIRE_INFO = 'UPDATE fire SET id = %s WHERE name = %s AND time >= %s::timestamp AND ' \
                           'time <= %s::timestamp;'
    # update fire info when: there are one fire in temp folder but records are from fireEvents with different name, one
    # record will be seperated into two records
    # so id in fire table need to be updated with a larger number

    # code for requesting fire information
    # get the last id from fire_history table
    SQL_GET_LASTEST_ID = 'SELECT MAX(id) FROM fire_history'
    # get the recent fire whose last record is within 10 days of the current date
    SQL_GET_LATEST_FIRE = 'SELECT a.id,h.year, h.state, h.name ' \
                          'from (SELECT id FROM fire_merged Where abs(DATE_PART(\'day\', ' \
                          'end_time - now())) < 10) a, fire_history h where h.id = a.id;'
    # return the aggregated fire information with a given id
    SQL_GET_LATEST_AGGREGATION = 'SELECT f.name, f.if_sequence,string_agg(distinct (f.agency), \', \'),f.state,f.id,' \
                                 'min(f.time),Max(f.time), st_astext(st_union(st_makevalid(f.geom_full))) as geom_full,' \
                                 'st_astext(st_union(st_makevalid(f.geom_1e4))),st_astext(st_union(st_makevalid(f.geom_1e3))),' \
                                 'st_astext(st_union(st_makevalid(f.geom_1e2))),st_astext(st_centroid(st_union(st_makevalid(f.geom_center)))), ' \
                                 'max(f.area) FROM (SELECT * FROM fire where id = {}) f Group by f.name, f.if_sequence, f.state, f.id'

    def create_history_table(self, conn: Connection) -> None:
        """
        Checks if the fire_history table exists,
        Creates fire_history table if not exist
        If it exists, the function does nothing
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

    def create_fire_table(self, conn: Connection) -> None:
        """
        Checks if the fire table exists
        Creates fire table if not exist
        If it exists, the function does nothing
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

    def create_fire_merged_table(self, conn: Connection) -> None:
        """
        Checks if the fire_merged table exists,
        Creates fire_merged table if not exist
        If it exists, the function does nothing
        :param conn: connection
        """
        # create a cursor
        cur = conn.cursor()
        # check if the fire_merged table exists
        # if the pipeline is run for the first time
        # then the fire_merged table will not exist
        # cur.execute(self.sql_check_if_fire_merged_table_exists)
        # tables = cur.fetchall()
        # table is the result of the statement: sql_check_if_history_table_exists
        if len(list(Connection.sql_execute(self.sql_check_if_fire_merged_table_exists))) == 0:
            # if table is empty, which means the fire_history table does not exists
            logger.info("No fire_merged table exists. Creating a new one.")
            cur.execute(FireDumper.sql_create_history_table)
            # create the fire_history table
            conn.commit()
            # commit the transaction so the change will be saved
            logger.info("fire_merged table created.")
        else:
            logger.info("Find the fire_merged table, continue >..")
        cur.close()

    def retrieve_all_fires(self) -> Set[tuple]:
        """
        Retrieves all fires in the database
        :return: set of tuples
        """
        with Connection() as connect:
            # check if the fire_history table exists
            # if not exist, executing sql_retrieve_all_fires will return an error
            self.create_history_table(connect)
            # retrieve all fires in fire_history
            result = set(Connection.sql_execute(self.sql_retrieve_all_fires))
            # result now is a set of tuples: (year, state, urlname)
            # e.g. for https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2015_fire_data/California/Deer_Horn_2/
            # the history tuple is : (2015, California, Deer_Horn_2)
        return result

    def insert(self, data: Dict) -> None:
        """
        Inserts a single fire record into fire table.
        :param data:dict to insert, from extractor.extract()
        :return:None
        """
        with Connection() as connect:
            # check if the fire table exists
            # if not exist, executing sql_insert will cause an error
            self.create_fire_table(connect)
            # create cursor
            cur = connect.cursor()
            # execute insert statement
            cur.execute(self.sql_insert_fire, data)
            connect.commit()
            # commit transaction
            # count number of records
            self.inserted_count = cur.rowcount()
            cur.close()
        # print logging message for debugging
        logger.info(f"Finished inserting file: {data['firename']}{data['datetime']}")
        logger.info(f"record count:{self.inserted_count}")

    def insert_history(self, year: int, name: str, state: str, id: int, current_year: int) -> None:
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
            # if year == current_year, then the fire's url year part is current_year_fire_data
            # if year != current_year, then the fire's url year part is the year as a string
            year_url = "current_year" if year == current_year else str(year)
            # make the dictionary to be inserted into fire_history
            data = {"year": year,
                    "firename": name,
                    "state": state,
                    "id": id,
                    "url": f"https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/{year_url}_fire_data/{state}/{name}/"}
            # create the cursor
            cur = connect.cursor()
            # execute insert statement
            cur.execute(self.sql_insert_fire_history, data)
            # commit transaction
            connect.commit()
            # close connection
            cur.close()

    def get_latest_fire_id(self) -> int:
        """
        Get the latest fire id to pass to the counter in data_from_fire
        :return: int
        """
        # execute select statement
        # the latest fire id is the first and only entry of the result
        return Connection.sql_execute(self.sql_get_lastest_id).__next__()[0]

    def get_recent_records(self) -> List[tuple]:
        """
        Return the list of ids of most recent records
        :return: List of tuples
        """
        with Connection() as conn:
            # create cursor
            cur = conn.cursor()
            # execute select statement to see if fire_merged table exists
            # if it doesn't exist, create one
            # if it exists, do nothing
            if len(list(Connection.sql_execute(self.sql_check_if_fire_merged_table_exists))) == 0:
                logger.info("No aggregated table exists. Creating a new one.")
                cur.execute(FireDumper.sql_create_fire_merged_table)
                conn.commit()
                logger.info("Aggregated table created successfully.")
            # execute select statement, get the fire ids of those fire whose end_date is within 10 days
            # these are fires that might update these days
            logger.info("Retrieving recent fires...")
            result = list(Connection.sql_execute(self.sql_get_latest_fire))
            logger.info(f"Fires updated within 10 days:{result}")
            # result is a list of tuples (id, year, state, urlname)
        return result

    @staticmethod
    def generate_data(aggregated_record: tuple, id: int):
        """
        Generates the data dictionary to pass to sql statement.
        :param aggregated_record: tuple
        :param id: int
        :return: Dict[str, str]
        """
        info = {"name": aggregated_record[0],
                "if_sequence": aggregated_record[1],
                "agency": aggregated_record[2],
                "state": aggregated_record[3],
                "id": id,
                "start_time": aggregated_record[5],
                "end_time": aggregated_record[6],
                "geom_full": aggregated_record[7],
                "geom_1e4": aggregated_record[8],
                "geom_1e3": aggregated_record[9],
                "geom_1e2": aggregated_record[10],
                "geom_center": aggregated_record[11],
                "max_area": aggregated_record[12]
                }
        fire_record_update = [info["id"], info["name"], info["start_time"], info["end_time"]]
        fire_merged_insert = [i for i in info.values()]
        return fire_record_update, fire_merged_insert

    def get_aggregated_fire_with_id(self, year: int, name: str, state: str, id: int, current_year: int) -> List[Tuple]:
        """
        Merges fire events with this id from fire table into several big fire events.
        :param year: int
        :param name: str
        :param state: str
        :param id: int
        :param current_year: int
        :return:
        """
        aggregated_with_id = list(Connection.sql_execute(self.sql_get_latest_aggregation.format(id)))
        if len(aggregated_with_id) == 0:
            logger.warning(f"Record {id} is an empty record. Skipping...")
            # if this id is an empty record, then there is no aggregated fire records
            # in this situation, we only mark the url as crawled, by inserting it into fire_history
            self.insert_history(year, name, state, id, current_year)
            # return the latest fire id
            raise InvalidRecordError
        logger.info(f"Successfully fetch Record #{id}, " + \
                    f"there are {len(aggregated_with_id)} aggregated records in this id")
        return aggregated_with_id

    def merge_fire_and_insert_history(self, id: int, year: int, name: str, state: str, current_year: int) -> int:
        '''
         A sequence of operations after inserting all records of a fire into fire table
         including insertion into fire_merged, fire_history
        :param id: int, id of the fire
        :param year:int
        :param name:str
        :param state:str
        :param current_year:int
        :return:int
        '''
        with Connection() as conn:
            cur = conn.cursor()
            # check if the fire_merged table exists, if not then create it
            # if it exists, do nothing
            self.create_fire_merged_table(conn)
            # get the aggregated record of the last fire inserted into fire table
            try:
                aggregated_with_id = self.get_aggregated_fire_with_id(year, name, state, id, current_year)
            except InvalidRecordError:
                return id
            # set a temporary value new_id as id
            new_id = id
            # the records can be dirty. Sometimes the folder of one fire includes fire with a different name
            # then when merged, the return list has more than one records
            # so a for loop is needed to deal with this situation
            for index_of_aggregated_record in range(len(aggregated_with_id)):
                new_id += index_of_aggregated_record
                # Most situation, there is only one record, new_id = id
                # if there is more than one, new_id will be id + i
                # create the dictionary for all values in aggregated record
                fire_info_update_params, fire_merged_insert_params = self.generate_data(aggregated_with_id
                                                                                        [index_of_aggregated_record],
                                                                                        new_id)
                # update their id in fire_info
                # here, if the new_id is different from id, the fire with that name will be updated with the new id
                cur.execute(self.sql_update_fire_info, fire_info_update_params)
                # insert this set in fire_aggregate
                cur.execute(self.sql_insert_fire_into_merged, fire_merged_insert_params)
                # commit the transaction
                conn.commit()
                # insert this set into fire_crawl_history, mark it as crawled
                self.insert_history(year, name, state, id, current_year)
        return new_id


if __name__ == '__main__':
    fd = FireDumper()


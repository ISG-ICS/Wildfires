"""
@author: Scarlett Zhang
This file has 2 classes:
InvalidRecordError
FireDumper
"""
from typing import List, Dict, Tuple
import logging
import rootpath
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection
from typing import Set, Any
from backend.data_preparation.crawler.fire_crawler import FireEvent

rootpath.append()


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
    SQL_CHECK_IF_TABLE_EXISTS = 'SELECT table_name FROM information_schema.TABLES WHERE table_name = \'{}\''

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
                        'geom_1e3, geom_1e2, geom_center, area) VALUES (%(firename)s,%(is_sequential)s,%(agency)s,' \
                        '%(state)s,%(fire_id)s,%(datetime)s,%(geopolygon_full)s,%(geopolygon_large)s,' \
                        '%(geopolygon_medium)s,%(geopolygon_small)s, ' \
                        'st_astext(st_centroid(st_geomfromtext(%(geopolygon_small)s))), %(area)s) ON CONFLICT DO NOTHING'
    # SQL_INSERT_FIRE: insert a new fire record into fire
    SQL_INSERT_FIRE_INTO_MERGED = 'INSERT INTO fire_merged(name, if_sequence, agency, state, id, start_time, ' \
                                  'end_time, geom_full, geom_1e4, geom_1e3, geom_1e2, geom_center, max_area)' \
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
    # retrieve all fire information
    SQL_RETRIEVE_ALL_FIRES = 'SELECT year,state,name FROM fire_history'
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

    @staticmethod
    def _get_length_of_select_query_result(query: str) -> int:
        """
        Takes a SELECT query and returns the number of rows the query returns.
        :param query: str.
                e.g. 'SELECT year,state,name FROM fire_history'
        :return: int
        """
        return sum(1 for _ in Connection.sql_execute(query))

    @staticmethod
    def _create_table(table_name: str):
        """
        Checks if the a given table exists,
        Creates fire_history table if not exist
        If it exists, the function does nothing
        :param table_name: name of the table to look for or create.
                Only 3 possible values: "fire_history", "fire", "fire_merged"
        """
        logger.info(f"Looking for {table_name} table in database...")
        # this is the select query from table name
        table_names_to_select_query = FireDumper.SQL_CHECK_IF_TABLE_EXISTS.format(table_name)
        # this is the create query from table name
        table_name_to_create_query = {
            "fire_history": FireDumper.SQL_CREATE_HISTORY_TABLE,
            "fire": FireDumper.SQL_CREATE_FIRE_TABLE,
            "fire_merged": FireDumper.SQL_CREATE_FIRE_MERGED_TABLE,
            "new_table_testing": "CREATE TABLE new_table_testing(tid int)"
        }[table_name]
        # check if the fire_history table exists
        # if the pipeline is run for the first time
        # then the fire_history table will not exist
        num_of_rows_found = FireDumper._get_length_of_select_query_result(table_names_to_select_query)
        # table is the result of the statement: sql_check_if_history_table_exists
        if num_of_rows_found == 0:
            # if table is empty, which means the fire_history table does not exists, so we create it
            logger.info(f"No {table_name} exists. Creating a new one.")
            Connection.sql_execute_commit(table_name_to_create_query)
            logger.info(f"Table {table_name} created.")
        else:
            logger.info(f"Found the {table_name} table, continue >..")

    # def _create_fire_table(self, conn: Connection):
    #     """
    #     Checks if the fire table exists
    #     Creates fire table if not exist
    #     If it exists, the function does nothing
    #     :param conn: Connection object
    #     """
    #     logger.info("Looking for fire table in database...")
    #     # create a cursor
    #     cur = conn.cursor()
    #     # check if the fire_history table exists
    #     # if the pipeline is run for the first time
    #     # then the fire_history table will not exist
    #     cur.execute(self.SQL_CHECK_IF_FIRE_TABLE_EXISTS)
    #     tables = cur.fetchall()
    #     # table is the result of the statement: sql_check_if_history_table_exists
    #     if len(tables) == 0:
    #         # if table is empty, which means the fire_history table does not exists
    #         logger.info("No fire table exists. Creating a new one.")
    #         cur.execute(FireDumper.SQL_CREATE_FIRE_TABLE)
    #         # create the fire_history table
    #         conn.commit()
    #         # commit the transaction so the change will be saved
    #         logger.info("Fire table created.")
    #     else:
    #         logger.info("Find the fire table, continue >..")
    #     cur.close()
    #
    # def _create_fire_merged_table(self, conn: Connection):
    #     """
    #     Checks if the fire_merged table exists,
    #     Creates fire_merged table if not exist
    #     If it exists, the function does nothing
    #     :param conn: Connection object
    #     """
    #     logger.info("Looking for fire_merged table in database...")
    #     # create a cursor
    #     cur = conn.cursor()
    #     # check if the fire_merged table exists
    #     # if the pipeline is run for the first time
    #     # then the fire_merged table will not exist
    #     # table is the result of the statement: sql_check_if_history_table_exists
    #     if len(list(Connection.sql_execute(self.SQL_CHECK_IF_FIRE_MERGED_TABLE_EXISTS))) == 0:
    #         # if table is empty, which means the fire_history table does not exists
    #         logger.info("No fire_merged table exists. Creating a new one.")
    #         cur.execute(FireDumper.SQL_CREATE_HISTORY_TABLE)
    #         # create the fire_history table
    #         conn.commit()
    #         # commit the transaction so the change will be saved
    #         logger.info("fire_merged table created.")
    #     else:
    #         logger.info("Find the fire_merged table, continue >..")
    #     cur.close()

    @staticmethod
    def retrieve_all_fires() -> Set[FireEvent]:
        """
        Retrieves all fires in the database.
        :return: set of FireEvent objects
                 e.g. [FireEvent(-1, 2015, 'California', 'FireA'), FireEvent(-1, 2015, 'California', 'FireB')]
        """
        # check if the fire_history table exists
        # if not exist, executing sql_retrieve_all_fires will return an error
        FireDumper._create_table("fire_history")
        # retrieve all fires in fire_history
        set_of_fire_event_objects = list(map(lambda fire_event_tuple: FireEvent.from_tuple(fire_event_tuple),
                                        Connection.sql_execute(FireDumper.SQL_RETRIEVE_ALL_FIRES)))
        # result now is a set of FireEvent objects
        # e.g. for https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2015_fire_data/California/Deer_Horn_2/
        # the FireEvent object is: Fire Event: Deer_Horn_2 in year 2015, state California
        return set_of_fire_event_objects

    @staticmethod
    def _generate_sql_statement_and_execute(sql_statement: str, data: Dict[str, Any]):
        """
        Generates a SQL statement with the data given as a dictionary and execute, commit the changes.
        :param sql_statement: string
                e.g. "SELECT * FROM fire_history WHERE %{id}=199"
        :param data: data as a dict.
                e.g. {'year': 2019, 'firename': 'TRESTLE', 'agency': 'USFS', 'datetime': .....}
        """
        with Connection() as conn:
            cur = conn.cursor()
            cur.execute(sql_statement, data)
            conn.commit()
            cur.close()
        return

    def insert(self, data: Dict[str, Any]):
        """
        Inserts a single fire record from FireExtractor.extract() into fire table.
        :param data:dict to insert, from extractor.extract()
                e.g. {'year': 2019, 'firename': 'TRESTLE', 'agency': 'USFS', 'datetime': .....}
        """
        logger.info(f"Inserting into fire table: {data['firename']} {data['datetime']}")
        # check if the fire table exists
        # if not exist, executing sql_insert will cause an error
        FireDumper._create_table("fire")
        FireDumper._generate_sql_statement_and_execute(FireDumper.SQL_INSERT_FIRE, data)
        logger.info(f"Finished inserting file: {data['firename']}{data['datetime']}")

    @staticmethod
    def insert_history(fire: FireEvent) -> None:
        """
        Inserts a fire record into fire_history table
        :param fire: a FireEvent object representing a wild fire event
                e.g. FireEvent(-1, 2015, 'California', 'FireQ')
        :return: None
        """
        logger.info(f"Inserting into fire_history table: {fire.url_name} in {fire.state} in {fire.year}")
        # make the dictionary to be inserted into fire_history
        FireDumper._generate_sql_statement_and_execute(FireDumper.SQL_INSERT_FIRE_HISTORY, fire.to_dict())
        logger.info(f"Finished inserting file: {fire.url_name} in {fire.state} in {fire.year}")

    @staticmethod
    def get_latest_fire_id() -> int:
        """
        Gets the latest fire id to pass to the counter in data_from_fire
        :return: int
                e.g. 299
        """
        # execute select statement
        # the latest fire id is the first and only entry of the result
        return Connection.sql_execute(FireDumper.SQL_GET_LASTEST_ID).__next__()[0]

    @staticmethod
    def get_recent_records() -> List[FireEvent]:
        """
        Return the list of ids of most recent records.
        :return: List of FireEvent objects
        e.g. [FireEvent(-1, 2015, 'California', 'FireA'), FireEvent(-1, 2015, 'California',"FireQ")]
        """
        # execute select statement to see if fire_merged table exists
        # if it doesn't exist, create one
        # if it exists, do nothing
        FireDumper._create_table("fire_merged")
        # execute select statement, get the fire ids of those fire whose end_date is within 10 days
        # these are fires that might update these days
        logger.info("Retrieving recent fires...")
        old_fires = list(map(lambda old_fire: FireEvent.from_tuple(old_fire),
                             Connection.sql_execute(FireDumper.SQL_GET_LATEST_FIRE)))
        logger.info(f"Fires updated within 10 days:{[str(old_fire) for old_fire in old_fires]}")
        return old_fires

    @staticmethod
    def _generate_data(aggregated_record: Tuple[Any], fire_id: int) -> Tuple[Dict[str, Any]]:
        """
        Generates the data dictionary to pass to sql statement.
        :param aggregated_record: tuple
                e.g. ("FireA",True,"USFA","California",999,minTime,maxTime,geom....,total_area)
        :param fire_id: int
                e.g. 998
        :return: Tuple[Dict[str, Any]]
                e.g. ({"name":"FireA"...}, {"name": "FireB"...})
        """
        # info = {"name": aggregated_record[0],
        #         #         "if_sequence": aggregated_record[1],
        #         #         "agency": aggregated_record[2],
        #         #         "state": aggregated_record[3],
        #         #         "id": id,
        #         #         "start_time": aggregated_record[5],
        #         #         "end_time": aggregated_record[6],
        #         #         "geom_full": aggregated_record[7],
        #         #         "geom_1e4": aggregated_record[8],
        #         #         "geom_1e3": aggregated_record[9],
        #         #         "geom_1e2": aggregated_record[10],
        #         #         "geom_center": aggregated_record[11],
        #         #         "max_area": aggregated_record[12]
        #         #         }
        columns = ["name", "if_sequence", "agency", "state", "id", "start_time", "end_time","geom_full", "geom_1e4",
                   "geom_1e3", "geom_1e2", "geom_center", "max_area"]
        info = dict(zip(columns, aggregated_record))
        info["id"] = fire_id
        fire_record_update = [info["id"], info["name"], info["start_time"], info["end_time"]]
        fire_merged_insert = [i for i in info.values()]
        return fire_record_update, fire_merged_insert

    def get_aggregated_fire_with_id(self, year: int, name: str, state: str, id: int) -> List[Tuple]:
        """
        Merges fire events with this id from fire table into several big fire events.
        Some pages might have fires from multiple fire events, so the return value is a list of tuples.
        If there are more than one fire events, then there will be multiple tuples in returned list.
        :param year: int
                e.g. 1999
        :param name: str
                e.g. "FireA"
        :param state: str
                e.g. "California"
        :param id: int
                e.g. 9999
        :return: list of tuples representing fire events
                e.g. [(1999, "FireA",...), (1999, "FireB",....)]
        """
        aggregated_fire_records_with_id = list(Connection.sql_execute(self.SQL_GET_LATEST_AGGREGATION.format(id)))
        if not aggregated_fire_records_with_id:
            logger.warning(f"Record {id} is an empty record. Skipping...")
            # if this id is an empty record, then there is no aggregated fire records
            # in this situation, we only mark the url as crawled, by inserting it into fire_history
            self.insert_history(FireEvent(year, state, name, id))
            # return the latest fire id
            raise InvalidRecordError
        logger.info(f"Successfully fetch Record #{id}, " + \
                    f"there are {len(aggregated_fire_records_with_id)} aggregated records in this id")
        return aggregated_fire_records_with_id

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
        self._create_table("fire_merged")
        try:
            aggregated_records_with_id = self.get_aggregated_fire_with_id(year, name, state, id)
        except InvalidRecordError:
            return id
        # set a temporary value new_id as id
        #new_id = id
        new_id = id - 1
        # the records can be dirty. Sometimes the folder of one fire includes fire with a different name
        # then when merged, the return list has more than one records
        # so a for loop is needed to deal with this situation
        for record_tuple in enumerate(aggregated_records_with_id):
            #new_id += index_of_aggregated_record
            new_id += 1
            # Most situation, there is only one record, new_id = id
            # if there is more than one, new_id will be id + i
            # create the dictionary for all values in aggregated record
            fire_info_update_params, fire_merged_insert_params = self._generate_data(record_tuple[1], new_id)
            # update their id in fire_info
            # here, if the new_id is different from id, the fire with that name will be updated with the new id
            self._generate_sql_statement_and_execute(self.SQL_UPDATE_FIRE_INFO, fire_info_update_params)
            # insert this set in fire_aggregate
            self._generate_sql_statement_and_execute(self.SQL_INSERT_FIRE_INTO_MERGED, fire_merged_insert_params)
            # insert this set into fire_crawl_history, mark it as crawled
            self.insert_history(FireEvent(year, state, name, id))
        # with Connection() as conn:
        #     cur = conn.cursor()
        #     # check if the fire_merged table exists, if not then create it
        #     # if it exists, do nothing
        #     self._create_table("fire_merged")
        #     # get the aggregated record of the last fire inserted into fire table
        #     try:
        #         aggregated_with_id = self.get_aggregated_fire_with_id(year, name, state, id, current_year)
        #     except InvalidRecordError:
        #         return id
        #     # set a temporary value new_id as id
        #     new_id = id
        #     # the records can be dirty. Sometimes the folder of one fire includes fire with a different name
        #     # then when merged, the return list has more than one records
        #     # so a for loop is needed to deal with this situation
        #     # 用enumerate
        #     for index_of_aggregated_record in range(len(aggregated_with_id)):
        #         new_id += index_of_aggregated_record
        #         # Most situation, there is only one record, new_id = id
        #         # if there is more than one, new_id will be id + i
        #         # create the dictionary for all values in aggregated record
        #         fire_info_update_params, fire_merged_insert_params = self.generate_data(*(aggregated_with_id
        #                                                                                 [index_of_aggregated_record]),
        #                                                                                 new_id)
        #         # update their id in fire_info
        #         # here, if the new_id is different from id, the fire with that name will be updated with the new id
        #         cur.execute(self.SQL_UPDATE_FIRE_INFO, fire_info_update_params)
        #         # insert this set in fire_aggregate
        #         cur.execute(self.SQL_INSERT_FIRE_INTO_MERGED, fire_merged_insert_params)
        #         # commit the transaction
        #         conn.commit()
        #         # insert this set into fire_crawl_history, mark it as crawled
        #         self.insert_history(year, name, state, id, current_year)
        return new_id


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    test_dumper = FireDumper()
    # Test for _create_table()
    # FireDumper.create_history_table("fire_merged")
    # Test for retrieve_all_fires()
    # print(list(map(lambda fire: str(fire), test_dumper.retrieve_all_fires())))
    # print(len(list(map(lambda fire: str(fire), test_dumper.retrieve_all_fires()))))
    # test_dumper.insert_history(FireEvent(1999,"Sss","sss",198888))
    # test_dumper.get_recent_records()
    # get_aggregated_fire_with_id()

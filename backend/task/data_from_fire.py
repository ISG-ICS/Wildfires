"""
@author: Scarlett Zhang
This file has 1 class:
DataFromFire: data pipeline for fire data.
"""
import os
import logging
from datetime import datetime
import datetime
import rootpath
import psycopg2
from paths import FIRE_DATA_DIR
from typing import Tuple, List
import time


from backend.task.runnable import Runnable
from backend.data_preparation.crawler.fire_crawler import FireCrawler, FireEvent
from backend.data_preparation.extractor.fire_extractor import FireExtractor, IncompleteShapefileError
from backend.data_preparation.dumper.fire_dumper import FireDumper

rootpath.append()
logger = logging.getLogger('TaskManager')


class DataFromFireRunnable(Runnable):
    """
    Run once per day/week/, not any time
    """
    def __init__(self):
        """
        Initialize runnable object
        """
        # crawler object initialization: can add more state names to crawl
        self.crawler = FireCrawler(["California"])
        # extractor object initialization
        self.extractor = FireExtractor()
        # dumper object initialization
        self.dumper = FireDumper()
        self.start_time = 2018

    @staticmethod
    def _create_temporary_data_path():
        """
        Checks if the temporary directory (FIRE_DATA_DIR) exists, if yes, do nothing
        if not, create the temporary directory.
        """
        # check if the FIRE_DATA_DIR exists,
        # this is the temporary directory to store fire shapefile downloaded from rmgsc
        if not os.path.isdir(FIRE_DATA_DIR):
            # if the temporary directory does not exist, create it
            logger.info(f"No fire data folder detected. Creating a new one at: {FIRE_DATA_DIR}")
            os.makedirs(FIRE_DATA_DIR)
        else:
            logger.info(f"Temp fire data folder detected, path: {FIRE_DATA_DIR}")

    @staticmethod
    def handle_fire_page_tuples(fire_page_tuple: Tuple[str], fire_id) -> Tuple[int, int, str, str]:
        """
        Takes a tuple of information about a fire web page and returns a tuple of unified information
        :param fire_page_tuple: Tuple
        :param fire_id: int
        :return: Tuple
        """
        if len(fire_page_tuple) == 4:
            # if it is a recent record
            fire_id, year, state, urlname = fire_page_tuple
            logger.info(f"Handling recent fire: old fire id:{fire_id}, year: {year}, state:{state}, urlname:{urlname}.")
        else:
            # if it is a new record
            year, state, urlname = fire_page_tuple
            logger.info(f"Handling new fire: fire id:{fire_id}, year: {year}, state:{state}, urlname:{urlname}.")
        return fire_id, year, state, urlname

    def merge_fire_and_return_fire_id(self, fire_id: int, year: int, urlname: str,state: str, current_year: int, errors: List[Tuple[int, int, str]]) -> int:
        """
        Merges a set of records of fire records into a single fire record for a time interval.
        :param fire_id: int
        :param year: int
        :param urlname: str
        :param state: str
        :param current_year: int
        :param errors: List[Tuple]
        :return: int
        """
        try:
            # insert the merged record into fire into fire_merged and fire_history
            # update the fire_id, since if there are actually multiple records,
            # fire_id need to increment more than 1
            return self.dumper.merge_fire_and_insert_history(fire_id, year, urlname, state, current_year)
        except psycopg2.errors.InternalError_:
            # Seldomly there is an InternalError_, when Union of geometry cause a self-intersection error
            logger.error(f"Internal Error: {fire_id}, {year}, {urlname}")
            # append this record into error list, for later manually insertion
            errors.append((fire_id, year, urlname))
            return fire_id

    def get_fire_id(self, entry: FireEvent, fire_id: int) -> int:
        """
        Gets the newest fire id for the next merged fire record.
        :param entry: Tuple
        :param fire_id: int
        :return: int
        """
        if entry.fire_id != -1:
            # if it is an updation for existing records, we need to access the latest fire id because the current
            # fire id is not the latest
            logger.info(f"Updated recent records: id {fire_id}, next fire id:{self.dumper.get_latest_fire_id() + 1}")
            return self.dumper.get_latest_fire_id() + 1
        else:
            # if it is a new fire, then just add 1 to the largest fire id
            return fire_id + 1

    @staticmethod
    def _generate_url_from_fire_event_object(fire_event: FireEvent) -> str:
        """
        Takes year, state, and url name and convert the entry to the url
        returns "https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2016_fire_data/California/Happy_Camp"
        :param fire_event: FireEvent. e.g. FireEvent(2017, 'California', 'Happy_Camp')
        :return: the url of this fire event on rmgsc.cr.usgs.gov
        """
        current_year = datetime.datetime.now().date().year
        year_str = "current_year" if fire_event.year == current_year else str(fire_event.year)
        return f"{FireCrawler.BASE_DIR}{year_str}_fire_data/{fire_event.state}/{fire_event.url_name}"

    # def _get_difference(a, b):
    #

    def run(self):
        """
        Interface for runnable
        """
        # get the current year, will be useful for converting year numbers from urls
        current_year = datetime.datetime.now().date().year
        # check if the FIRE_DATA_DIR exists,
        self._create_temporary_data_path()
        # Here we need to get all useful fire urls
        # sometimes rmgsc doesn't response, so we set a while loop to continue until we get the information
        try:
            all_fire_tuples = self.crawler.extract_all_fires(self.start_time)
        except RuntimeError:
            logger.error("Stopping data pipeline. No network connection.")
            return
        # retrieve all historical links from fire_history table
        logger.info("Retrieving historical fires...")
        crawled = set(self.dumper.retrieve_all_fires())
        logger.info(f"Num of historical links: {len(crawled)}")
        # get the difference between all links and crawled
        to_crawl = sorted(list(crawled.difference(set(all_fire_tuples))), key=lambda fire_event: fire_event.url_name)
        logger.info(f"Num of new links: {len(to_crawl)}")
        logger.info("Requesting recent records...")
        # get the fires that updated recently(in 10 days)
        # because they might have been updated after last time this pipeline run
        recent_records = self.dumper.get_recent_records()
        logger.info(f"Recent records: {recent_records}")
        # final list of urls we need to crawl is the combination of un-crawled links and recent links
        to_crawl = recent_records + to_crawl
        logger.info(f"Total number of fire urls needed to be crawled: {len(to_crawl)}")
        logger.info(f"To be crawled urls:{[str(fire_event) for fire_event in to_crawl]}")
        # clean up the temporary directory, in case of a dirty directory
        self.crawler.cleanup()
        # records with errors are stored in errors list for a backup
        errors = []
        # get the latest fire_id, if there is no fire id exists, then fire_id = 0
        fire_id = 0 if self.dumper.get_latest_fire_id() is None else int(self.dumper.get_latest_fire_id() + 1)
        logger.info(f"Initial fire id: {fire_id}")
        # entries in to_crawl are:
        # New tuples: new tuples that is never crawled: (year, state, urlname)
        # Recent tuples: tuples of recent fires: (old_id, year, state, urlname)
        for entry in to_crawl:
            # if statement take forward here, handle 3 or 4 values
            logger.info(f"Now working on: {entry}")
            fire_id, year, state, urlname = entry.to_tuple(fire_id)
            # generate the url from known information
            # download all records to temporary directory
            self.crawler.crawl(entry.to_url())
            # if the temporary directory has more than one sub directory(records), then the fire is a sequence of fire
            if_sequence = False if len([f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]) == 1 else True
            # for each record in the temporary directory:
            for record in [f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]: # glob
                absolute_path_folder = os.path.join(FIRE_DATA_DIR, record)
                # extract the shapefile into a dictionary called single_record
                try:
                    single_record = self.extractor.extract(absolute_path_folder, if_sequence, fire_id, state)
                except IncompleteShapefileError as err:
                    # the extractor result can be empty when the record is incomplete and cannot be decoded
                    # in this situation, skip the record
                    logger.warning(str(err))
                    continue
                # insert the single record into fire table
                self.dumper.insert(single_record)
                logger.info(f"Successfully inserted {record} into fire_info.")
            # after the for loop, all records belongs to this fire should be inserted into fire
            # then we can create the merged record and insert it into fire_merged and mark it as crawled in fire_history
            fire_id = self.merge_fire_and_return_fire_id(fire_id, year, urlname, state, current_year, errors)
            fire_id = self.get_fire_id(entry, fire_id)
            logger.info(f"New fire id : {fire_id}")
            # clean up the temporary directory for crawling the next fire record
            self.crawler.cleanup()
        # finished all insertion
        logger.info("Finished running. Waiting for one day.")
        logger.info(f"Error in : {errors}")
        return


if __name__ == '__main__':
    # print logging into console, for debugging ONLY
    # commit it out when run on server
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    a = FireEvent(33,"aa","ss",-1)
    b = FireEvent(33,"bb","ss",-1)
    c = FireEvent(33,"aa","ss",-1)
    print(set((a,b)).difference(set([c])))
    while True:
        DataFromFireRunnable().run()
        # sleep one day
        time.sleep(3600 * 24)
        logger.info("Finished running. Waiting for one day.")
    # fe = FireExtractor()
    # fd = FireDumper()
    # fd.insert(fe.extract("C:\myResearch\Wildfires\data\\fire-data\ca_trestle_20190605_1200_dd83",True, 0, "ss"))



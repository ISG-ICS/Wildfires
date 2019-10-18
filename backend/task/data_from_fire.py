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

rootpath.append()


from backend.task.runnable import Runnable
from backend.data_preparation.crawler.fire_crawler import FireCrawler, FireEvent
from backend.data_preparation.extractor.fire_extractor import FireExtractor, IncompleteShapefileError
from backend.data_preparation.dumper.fire_dumper import FireDumper

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

    def merge_fire_and_return_fire_id(self, fire_id: int, year: int, urlname: str,state: str, current_year: int, errors: List[Tuple[int, int, str]]) -> int:
        """
        Merges a set of records of fire records into a single fire record for a time interval.
        :param fire_id: int
                e.g. 999
        :param year: int
                e.g. 2016
        :param urlname: str
                e.g. "FireQ"
        :param state: str
                e.g."California"
        :param current_year: int
                e.g.2019
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

    def get_fire_id(self, fire_event: FireEvent, fire_id: int) -> int:
        """
        Gets the newest fire id for the next merged fire record.
        :param fire_event: Tuple
        :param fire_id: int
        :return: int
        """
        if fire_event.fire_id != -1:
            # if it is an updation for existing records, we need to access the latest fire id because the current
            # fire id is not the latest
            logger.info(f"Updated recent records: id {fire_id}, next fire id:{self.dumper.get_latest_fire_id() + 1}")
            return self.dumper.get_latest_fire_id() + 1
        else:
            # if it is a new fire, then just add 1 to the largest fire id
            return fire_id + 1

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
        # get the difference between all links and crawled
        to_crawl = sorted((set(all_fire_tuples).difference(set(self.dumper.retrieve_all_fires()))),
                          key=lambda fire_event: fire_event.url_name)
        logger.info(f"Num of new links: {len(to_crawl)}")
        logger.info("Requesting recent records...")
        # get the fires that updated recently(in 10 days)
        # because they might have been updated after last time this pipeline run
        recent_records = self.dumper.get_recent_records()
        logger.info(f"Recent records: {recent_records}")
        # final list of urls we need to crawl is the combination of un-crawled links and recent links
        to_crawl += recent_records
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
        for fire_event in to_crawl:
            # if statement take forward here, handle 3 or 4 values
            logger.info(f"Now working on: {fire_event}")
            fire_id, year, state, urlname = fire_event.to_tuple(fire_id)
            # generate the url from known information
            # download all records to temporary directory
            self.crawler.crawl(fire_event.to_url())
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
            fire_id = self.get_fire_id(fire_event,
                      self.merge_fire_and_return_fire_id(fire_id, year, urlname, state, current_year, errors))
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
    while True:
        DataFromFireRunnable().run()
        # sleep one day
        time.sleep(3600 * 24)
        logger.info("Finished running. Waiting for one day.")



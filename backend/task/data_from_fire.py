import os
import logging
from datetime import datetime
import datetime
import rootpath
import psycopg2
from paths import FIRE_DATA_DIR
import time

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.crawler.fire_crawler import FireCrawler
from backend.data_preparation.extractor.fire_extractor import FireExtractor
from backend.data_preparation.dumper.fire_dumper import FireDumper

logger = logging.getLogger('TaskManager')


class DataFromFire(Runnable):
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

    def run(self):
        """
        Interface for runnable
        """
        # get the current year, will be useful for converting year numbers from urls
        current_year = datetime.datetime.now().date().year
        # check if the FIRE_DATA_DIR exists,
        # this is the temporary directory to store fire shapefile downloaded from rmgsc
        if not os.path.isdir(FIRE_DATA_DIR):
            # if the temporary directory does not exist, create it
            logger.info(f"No fire data folder detected. Creating a new one at: {FIRE_DATA_DIR}")
            os.makedirs(FIRE_DATA_DIR)
        else:
            logger.info(f"Temp fire data folder detected, path: {FIRE_DATA_DIR}")
        # Here we need to get all useful fire urls
        # sometimes rmgsc doesn't response, so we set a while loop to continue until we get the information
        while True:
            try:
                logger.info("Attempting to get all links...")
                all_fire_tuples = self.crawler.extract_all_fires()
            except:
                logger.info("Attempt failed. Retrying...")
                continue
            break
        # filter out links that is too old or that contains no useful information(those with name ActivePerim)
        for year_state_name_tuples in all_fire_tuples[:]:
            if year_state_name_tuples[0] < 2015 or year_state_name_tuples[2] == "ActivePerim":
                all_fire_tuples.remove(year_state_name_tuples)
        # retrieve all historical links from fire_history table
        logger.info("Retrieving historical fires...")
        crawled = set(self.dumper.retrieve_all_fires())
        logger.info(f"Num of historical links: {len(crawled)}")
        # get the difference between all links and crawled
        to_crawl = sorted(list(set(all_fire_tuples).difference(crawled)))
        logger.info(f"Num of new links: {len(to_crawl)}")
        logger.info("Requesting recent records...")
        # get the fires that updated recently(in 10 days)
        # because they might have been updated after last time this pipeline run
        recent_records = self.dumper.get_recent_records()
        logger.info(f"Recent records: {recent_records}")
        # final list of urls we need to crawl is the combination of uncrawled links and recent links
        to_crawl = recent_records + to_crawl
        logger.info(f"Total number of fire urls needed to be crawled: {len(to_crawl)}")
        logger.info(f"To be crawled urls:{to_crawl}")
        # clean up the temporary directory, in case of a dirty directory
        self.crawler.cleanup()
        # records with errors are stored in errors list for a backup
        errors = []
        # get the latest fire_id, if there is no fire id exists, then fire_id = 0
        fire_id = 0 if self.dumper.get_latest_fire_id() == None else int(self.dumper.get_latest_fire_id() + 1)
        logger.info(f"Initial fire id: {fire_id}")
        # entries in to_crawl are:
        # TYPE 1: new tuples that is never crawled: (year, state, urlname)
        # TYPE 2: tuples of recent fires: (old_id, year, state, urlname)
        for entry in to_crawl:
            logger.info(f"Now working on: {entry}")
            if len(entry) == 4:
                # if it is a TYPE 2 record
                fire_id = entry[0]
                year = entry[1]
                state = entry[2]
                urlname = entry[3]
                logger.info(f"Updating recent fire: old fire id:{fire_id}, year: {year}, state:{state}, urlname:{urlname}.")
            else:
                # if it is a TYPE 1 record
                year = entry[0]
                state = entry[1]
                urlname = entry[2]
                logger.info(f"Updating new fire: fire id:{fire_id}, year: {year}, state:{state}, urlname:{urlname}.")
            # generate the url from known information
            url = self.crawler.generate_url_from_tuple(year, state, urlname, current_year)
            # download all records to temporary directory
            self.crawler.crawl(url)
            # if the temporary directory has more than one sub directory(records), then the fire is a sequence of fire
            if_sequence = False if len([f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]) == 1 else True
            # for each record in the temporary directory:
            for record in [f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]:
                absolute_path_folder = os.path.join(FIRE_DATA_DIR, record)
                # extract the shapefile into a dictionary called single_record
                single_record = self.extractor.extract(absolute_path_folder, record, if_sequence, fire_id, state)
                if single_record == dict():
                    # the extractor result can be empty when the record is incomplete and cannot be decoded
                    # in this situation, skip the record
                    logger.info(f"Hit incomplete polygon files, skipping. ")
                    continue
                # insert the single record into fire table
                self.dumper.insert(single_record)
                logger.info(f"Successfully inserted {record} into fire_info.")
            # after the for loop, all records belongs to this fire should be inserted into fire
            # then we can create the merged record and insert it into fire_merged and mark it as crawled in fire_history
            try:
                # insert the merged record into fire into fire_merged and fire_history
                # update the fire_id, since if there are actually multiple records,
                # fire_id need to increment more than 1
                fire_id = self.dumper.after_inserting_into_fire_info(fire_id,year,urlname,state,current_year)
            except psycopg2.errors.InternalError_:
                # Seldomly there is an InternalError_, when Union of geometry cause a self-intersection error
                logger.error(f"Internal Error: {fire_id}, {year}, {urlname}")
                # append this record into error list, for later manually insertion
                errors.append((fire_id, year, urlname))
            if len(entry) == 4:
                # if it is an updation for existing records, we need to access the latest fire id because the current
                # fire id is not the latest
                logger.info(f"Updated recent records: id {fire_id}, next fire id:{self.dumper.get_latest_fire_id() + 1}")
                fire_id = self.dumper.get_latest_fire_id() + 1
            else:
                # if it is a new fire, then just add 1 to the largest fire id
                fire_id += 1
            logger.info(f"New fire id : {fire_id}")
            # clean up the temporary directory for crawling the next fire record
            self.crawler.cleanup()
        # finished all insertion
        logger.info("Finished Crawling")
        logger.info(f"Error in : {errors}")
        return





if __name__ == '__main__':
    # print logging into console, for debugging ONLY
    # commit it out when run on server
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    while True:
        DataFromFire().run()
        # sleep one day
        time.sleep(3600 * 24)


import os
import logging
from datetime import datetime
import datetime
import rootpath
import psycopg2
from paths import FIRE_DATA_DIR

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.crawler.fire_crawler import FireCrawler
from backend.data_preparation.extractor.fire_extractor import FireExtractor
from backend.data_preparation.dumper.fire_dumper import FireDumper

logger = logging.getLogger('TaskManager')


class DataFromFire(Runnable):
    """run once per day/week/, not any time"""
    def __init__(self):
        self.crawler = FireCrawler(["California"])
        self.extractor = FireExtractor()
        self.dumper = FireDumper()
        self.explored_year = set()
        self.explored_fire = set()
        self.logfile = ""


    def write_log(self):
        pass
    def run(self):
        """
        Interface for runnable
        """
        current_year = datetime.datetime.now().date().year
        if not os.path.isdir(FIRE_DATA_DIR):
            logger.info(f"No fire data folder detected. Creating a new one at: {FIRE_DATA_DIR}")
            os.makedirs(FIRE_DATA_DIR)
        else:
            logger.info(f"Temp fire data folder detected, path: {FIRE_DATA_DIR}")
        while True:
            try:
                logger.info("Attempting to get all links...")
                all_fire_tuples = self.crawler.extract_all_fires()
            except:
                logger.info("Attempt failed. Retrying...")
                continue
            break
        for year_state_name_tuples in all_fire_tuples[:]:
            if year_state_name_tuples[0] < 2015 or year_state_name_tuples[2] == "ActivePerim":
                all_fire_tuples.remove(year_state_name_tuples)
        logger.info("Retrieving historical fires...")
        crawled = set(self.dumper.retrieve_all_fires())
        logger.info(f"Num of historical links: {len(crawled)}")
        # get the difference between all links and crawled
        to_crawl = sorted(list(set(all_fire_tuples).difference(crawled)))
        logger.info(f"Num of new links: {len(to_crawl)}")
        logger.info("Requesting recent records...")
        recent_records = self.dumper.get_recent_records()
        logger.info(f"Recent records: {recent_records}")
        to_crawl = recent_records + to_crawl
        logger.info(f"Total number of fire urls needed to be crawled: {len(to_crawl)}")
        logger.info(f"To be crawled urls:{to_crawl}")
        self.crawler.cleanup()
        errors = []
        fire_id = 0 if self.dumper.get_latest_fire_id() == None else int(self.dumper.get_latest_fire_id() + 1)
        logger.info(f"Initial fire id: {fire_id}")
        for entry in to_crawl:
            logger.info(f"Now working on: {entry}")
            if len(entry) == 4:
                fire_id = entry[0]
                year = entry[1]
                state = entry[2]
                urlname = entry[3]
                logger.info(f"Updating recent fire: old fire id:{fire_id}, year: {year}, state:{state}, urlname:{urlname}.")
            else:
                year = entry[0]
                state = entry[1]
                urlname = entry[2]
                logger.info(f"Updating new fire: fire id:{fire_id}, year: {year}, state:{state}, urlname:{urlname}.")
            url = self.crawler.generate_url_from_tuple(year, state, urlname, current_year)
            self.crawler.crawl(url)
            if_sequence = False if len([f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]) == 1 else True
            for record in [f for f in os.listdir(FIRE_DATA_DIR) if not f.startswith('.')]:
                absolute_path_folder = os.path.join(FIRE_DATA_DIR, record)
                single_record = self.extractor.extract(absolute_path_folder, record, if_sequence, fire_id, state)
                if single_record == dict():
                    logger.info(f"Hit incomplete polygon files, skipping. ")
                    continue
                self.dumper.insert(single_record)
                logger.info(f"Successfully inserted {record} into fire_info.")
            try:
                fire_id = self.dumper.after_inserting_into_fire_info(fire_id,year,urlname,state,current_year)
            except psycopg2.errors.InternalError_:
                logger.error(f"Internal Error: {fire_id}, {year}, {urlname}")
                errors.append((fire_id, year, urlname))
            if len(entry) == 4:
                logger.info(f"Updated recent records: id {fire_id}, next fire id:{self.dumper.get_latest_fire_id() + 1}")
                fire_id = self.dumper.get_latest_fire_id() + 1
            else:
                fire_id += 1
            logger.info(f"New fire id : {fire_id}")
            self.crawler.cleanup()
        # finished all insertion
        logger.info("Finished Crawling")
        logger.info(f"Error in : {errors}")
        return





if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    DataFromFire().run()


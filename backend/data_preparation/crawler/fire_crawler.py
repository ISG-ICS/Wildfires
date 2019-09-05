"""
@author: Scarlett Zhang
This file contains 1 classes:
1. class FireCrawler: the crawler class for fire information
"""
import re
import requests
import rootpath
import wget
import os
import datetime
import logging
import shutil
import urllib.error
import glob
from typing import List, Set
from paths import FIRE_DATA_DIR
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from retrying import retry

rootpath.append()

logger = logging.getLogger('TaskManager')


class CannotCrawlException(Exception):
    pass



class FireEvent:
    # the class to represent a FireEvent object, a fire event is a link on the rmgsc website
    def __init__(self, year: int, state: str, url_name: str):
        """
        Takes year, state, url_name and make a new FireEvent object
        :param year: the year when the fire event occurred.
                e.g. 2017
        :param state: the state where the fire event occurred.
                e.g. 'California'
        :param url_name: the name of this fire event on rmgsc website, should contains underscore.
                e.g. "Happy_Camp_Mountain"
        """
        self.fire_id = -1
        self.year = year
        self.state = state
        self.url_name = url_name

    def is_valid(self) -> bool:
        """
        Judges if this fire event is valid. A valid fire event should have reasonable fire name.
        :return: bool
        """
        # to delete exceptions: "[To Parent Directory]" "whatever.zip"
        # ActivePerim is an useless link which contains metadata over the year, existing in links before 2016 Skip it
        return "." in self.url_name or "[To Parent Directory]" == self.url_name or self.url_name == "ActivePerim"

    def __str__(self) -> str:
        """
        Transforms a FireEvent into a string.
        :return: str
        """
        return f"Fire Event: {self.url_name} in year {self.year}, state {self.state}"


class FireCrawler(CrawlerBase):
    # BASE_DIR is the website directory the crawler will crawl
    BASE_DIR = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
    RE_EXTRACT_FIRE_EVENTS_IN_STATE = re.compile(r'<A .*?>(.*?)</A>', re.S | re.M)
    RE_EXTRACT_ALL_FIRES = re.compile(r'<A .*?>(\w*?)</A>', re.S | re.M)
    RE_EXTRACT_FILES_IN_FIRE_EVENTS = re.compile(r'<A .*?>([a-z]{2}_.+?)</A>', re.S | re.M)

    def __init__(self, states: List[str]):
        """
        Initialization for the crawler.
        :param states: list of states that the crawler needs to crawl
                e.g. ["California", "Nevada"]
        """
        super().__init__()
        self.states = states
        # states is a list of states that the crawler needs to crawl

    @staticmethod
    @retry(retry_on_exception=requests.exceptions.RequestException, stop_max_attempt_number=3)
    def _get_url(url: str, page_name: str, function_name: str) -> str:
        """
        Helper function for request.get().
        When request.get() meets the connection error, it will retry.
        If retry fails for 5 attempts, it will throw RuntimeError.
        :param url: str,
                e.g. 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
        :param page_name: str,
                e.g. 'main_page'
        :param function_name: str,
                e.g. 'extract_all_fires()'
        :return: str,
                e.g. the string of all HTML code from 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
        """
        logger.info(f"Fetching {page_name} page in function {function_name}...")
        response = requests.get(url).content.decode("utf-8")
        logger.info(f"Finished fetching {page_name} page in function {function_name}")
        return response

    @staticmethod
    @retry(retry_on_exception=urllib.error.URLError, stop_max_attempt_number=3)
    def _download_single_file(url: str, file: str, out_path: str):
        """
        Downloads a single file from the website to the out_path.
        :param url: url of the fire event.
               e.g. https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2017_fire_data/California/Eclipse/
        :param file: file name of the file to download.
                e.g. 'ca_eclipse_20170823_0000_dd83.cpg'
        :param out_path: path where the downloaded file stored.
                e.g. '/myResearch/Wildfires/data/fire-data'
        """
        logger.info(f"Downloading {url}/{file} to {out_path}.")
        wget.download(url=url + "/" + file, out=out_path)
        logger.info(f"Finished Downloading {url}/{file} to {out_path}.")

    @staticmethod
    @retry(retry_on_exception=requests.exceptions.RequestException, stop_max_attempt_number=3)
    def _extract_fire_events_in_state(year: int, state: str) -> List[FireEvent]:
        """
        Takes a year, and a state, fetches all fire events in that year and the state and output it as a list of
        FireEvent objects.
        :param year: int, represent the year to crawl.
                e.g. 2017
        :param state: str, the state to crawl.
                e.g. 'California'
        :return: list of FireEvent objects of all fire events happened in that year this state
                e.g. [FireEvent(2015, 'California', 'FireA'), FireEvent(2015, 'California', 'FireB')]
        """
        logger.info(f"Fetching fire events in {state} in year {year}.")
        # try except for network errors
        # try:
        #      fire_events_page_in_state = FireCrawler._get_url(f"{FireCrawler.BASE_DIR}{year}_fire_data/{state}",
        #                                         f"{state} State of year {year}", "_extract_fire_events_in_state()")
        # except requests.exceptions.RequestException:
        #     logger.error(f"Error: cannot fetch state page for {state} in {year}")
        #     # retry
        # else:
        #     # crawl the all fires in this state
        #     # This re_formula is different from the one used
        #     fire_names_in_this_state = FireCrawler.RE_EXTRACT_FIRE_EVENTS_IN_STATE.findall(fire_events_page_in_state)
        #     logger.info(f"Finished fetching fire events in {state} in year {year}.")
        #     return list(map(lambda single_fire_name: FireEvent(year, state, single_fire_name), fire_names_in_this_state))
        fire_events_page_in_state = FireCrawler._get_url(f"{FireCrawler.BASE_DIR}{year}_fire_data/{state}",
                                                         f"{state} State of year {year}",
                                                         "_extract_fire_events_in_state()")
        fire_names_in_this_state = FireCrawler.RE_EXTRACT_FIRE_EVENTS_IN_STATE.findall(fire_events_page_in_state)
        logger.info(f"Finished fetching fire events in {state} in year {year}.")
        return list(map(lambda single_fire_name: FireEvent(year, state, single_fire_name), fire_names_in_this_state))

    @staticmethod
    def _filter_out_invalid_fire_events(fires: List[FireEvent]):
        """
        Find those invalid FireEvent objects and remove them from the input list
        :param fires: list of FireEvent objects.
                e.g. [FireEvent(2015, 'California', 'FireA'), FireEvent(2015, 'California', 'FireB')]
        """
        for fire_event in fires[:]:
            if fire_event.is_valid():
                fires.remove(fire_event)

    def extract_all_fires(self, start_year: int) -> List[FireEvent]:
        """
        Extracts all fires on the website and return.
        The returned value is a list of tuples:(year:int, state:string, fire's name in its url)
        :param start_year: int, start year for the crawler. Record before the start year will be deleted.
                e.g. 2015
        :return: list of FireEvent objects
                e.g. [FireEvent(2015, 'California', 'FireA'), FireEvent(2015, 'California', 'FireB')]
        """
        logger.info("Attempting to get all links...")
        current_year = datetime.datetime.now().date().year
        # fetch all year nodes from the website, may encounter errors
        # add a try-except block, and while loop to keep trying
        # if attempts > 3 raise an exception
        try:
            main_page = self._get_url(FireCrawler.BASE_DIR, "main_page", "extract_all_fires()")
        except requests.exceptions.RequestException:
            logger.error("Error: Cannot fetch main_page in function extract_all_fires()")
            raise CannotCrawlException("Error: Cannot fetch main_page in function extract_all_fires")
            # retry exception
        else:
            # the last node is "historical_fire_data" and we don't want it
            sub_links_of_each_year = FireCrawler.RE_EXTRACT_ALL_FIRES.findall(main_page)[:-1]
            # sub_links_of_each_year are now fire data of a certain year or current year
            # e.g. '2010_fire_data', 'current_year_fire_data'
            fires = []
            for sub_link_of_each_year in sub_links_of_each_year:
                # sub_link_of_each_year: e.g. '2010_fire_data'
                # to change "current_year" to the real year as an integer
                year_as_int = current_year if sub_link_of_each_year == "current_year_fire_data" \
                                         else int(sub_link_of_each_year.split("_")[0])
                # ignore years that before the start year
                # filter out links that is too old
                if year_as_int >= start_year:
                    for state in self.states:
                        # for each state, extract fire events in that year at that state
                        fires.extend(self._extract_fire_events_in_state(year_as_int, state))
            self._filter_out_invalid_fire_events(fires)
            return fires

    @staticmethod
    def _download_fire_record(single_file_name: str, used_folder_names: Set[str], url_of_fire_event: str):
        """
        Downloads a single fire record from the website and puts its sub-files into a folder.
        :param single_file_name: e.g. "ca_cedar_20170810_0000_dd83.CPG"
        :param used_folder_names:e.g. ("ca_cedar_20170810_0000_dd83", "ca_cedar_20170812_2145_dd83")
        :param url_of_fire_event:e.g "https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2017_fire_data/California/Cedar/"
        """
        if not ".zip" == single_file_name[-4:]:
            # if it is a zip don't download
            folder_name = single_file_name.split(".")[0]
            if folder_name not in used_folder_names:
                # if the folder name is not in used_folder_names, which means it is a new folder
                # then create the folder and add it into the used_folder_names set, to avoid duplicate folders
                used_folder_names.add(folder_name)
                os.makedirs(os.path.join(FIRE_DATA_DIR, folder_name))
            out_path = os.path.join(FIRE_DATA_DIR, folder_name)
            FireCrawler._download_single_file(url_of_fire_event, single_file_name, out_path)

    @staticmethod
    @retry(retry_on_exception=requests.exceptions.RequestException, stop_max_attempt_number=3)
    def _extract_file_names_in_fire_event(url_of_fire_event: str) -> List[str]:
        """
        Extracts all file names from a fire_event page. Return a list of all file names.
        :param url_of_fire_event: the url of the fire_event
                e.g. https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2017_fire_data/California/Antelope/
        :return: e.g. ["ca_antelope_20170706_1930_dd83.CPG", "ca_antelope_20170706_1930_dd83.dbf"]
        """
        # try:
        #     fire_page = FireCrawler._get_url(url_of_fire_event, url_of_fire_event, "crawl()")
        # except requests.exceptions.RequestException:
        #     logger.error(f"Error: cannot fetch fire page {url_of_fire_event}")
        fire_page = FireCrawler._get_url(url_of_fire_event, url_of_fire_event, "crawl()")
        return FireCrawler.RE_EXTRACT_FILES_IN_FIRE_EVENTS.findall(fire_page)

    def crawl(self, url_of_fire_event: str):
        """
        Takes the url string of one fire and start to crawl all files.
        :param url_of_fire_event: str
                e.g. "https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2016_fire_data/California/Happy_Camp"
        """
        used_folder_names = set()
        # grab all fire names in the page
        # for loop for runtime error
        # download useful files
        for file in FireCrawler._extract_file_names_in_fire_event(url_of_fire_event):
            self._download_fire_record(file, used_folder_names, url_of_fire_event)
        return

    @staticmethod
    def cleanup():
        """
        Cleans up the temp data folder
        """
        logger.info("Cleaning up the temp data folder...")
        folder_names = glob.glob(os.path.join(FIRE_DATA_DIR, "[a-z]*"))
        for folder_name in folder_names:
            shutil.rmtree(folder_name)
        logger.info("Finished cleaning up the temp data folder.")


if __name__ == '__main__':
    # module tester
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    test_crawler = FireCrawler(["California"])
    #test_crawler._extract_fire_events_in_state(2015, "California")
    print(list(map(lambda fire: str(fire), test_crawler.extract_all_fires(2015))))
    used = set()
    # FireCrawler.download_fire_record('ca_eclipse_20170823_0000_dd83.cpg', used, "https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2017_fire_data/California/Eclipse/")
    # FireCrawler.download_fire_record('ca_eclipse_20170823_0000_dd83.dbf', used, "https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2017_fire_data/California/Eclipse/")
    # test_crawler.crawl("https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2015_fire_data/California/Chorro/")
    test_crawler.cleanup()
    # fire_list = test_crawler.extract_all_fires()
    # random_number = random.randint(0, len(fire_list))
    # random_entry = fire_list[random_number]
    # random_url = test_crawler.generate_url_from_tuple(random_entry[0], random_entry[1],random_entry[2], 2019)
    # test_crawler.crawl(random_url)

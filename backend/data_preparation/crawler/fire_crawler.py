"""
@author: Scarlett Zhang
This file contains 1 classes:
1. class FireCrawler: the crawler class for fire information
"""
import datetime
import glob
import logging
import os
import re
import shutil
from typing import Dict, Any
from typing import List, Set, Tuple

import requests
import rootpath
import wget
from retrying import retry

rootpath.append()

from paths import FIRE_DATA_DIR
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.extractor.fire_extractor import FireExtractor, IncompleteShapefileError

logger = logging.getLogger('TaskManager')


class FireCrawlException(Exception):
    pass


class FireEvent:
    """
    This class is to represent a FireEvent object, a fire event is a link on the rmgsc website.
    """

    def __init__(self, year: int, state: str, url_name: str, fire_id=-1):
        """
        Takes year, state, url_name and make a new FireEvent object
        :param year: the year when the fire event occurred.
                e.g. 2017
        :param state: the state where the fire event occurred.
                e.g. 'California'
        :param url_name: the name of this fire event on rmgsc website with all spaces substituted by underscores.
                e.g. "Happy_Camp_Mountain"
        :param fire_id: the id of the fire event in database, -1 for new fire events that is not inserted into the
                database
        """
        self.fire_id = fire_id
        self.year = year
        self.state = state
        self.url_name = url_name

    def __eq__(self, other):
        return self.year == other.year and self.state == other.state and self.url_name == other.url_name

    def __hash__(self):
        return hash(self.to_url())

    @classmethod
    def from_tuple(cls, tuple_for_information: Tuple[Any]):
        """
        Generates a FireEvent object from a tuple of information.
        :param tuple_for_information: Tuple.
               e.g. (2015, 'California', 'Happy_Camp'), (111, 2017, 'California', 'Eclipse')
        :return: FireEvent object.
               e.g. FireEvent(-1, 2015, 'California', 'Happy_Camp'), FireEvent(111, 2017, 'California', 'Eclipse')
        """
        if len(tuple_for_information) == 3:
            return cls(*tuple_for_information)
        else:
            return cls(*tuple_for_information[1:], tuple_for_information[0])

    def is_invalid(self) -> bool:
        """
        Judges if this fire event is valid. A valid fire event should have reasonable fire name.

        to delete exceptions like:

        "[To Parent Directory]":
                shows on all pages as the link to the parent page
        "whatever.zip": some dirty data sources have zip files of all fires in the directory of the year listed among
                links to fire events
        "ActivePerim": an useless link which contains metadata over the year, existing in links before 2016 Skip it
                if a link looks like the above 3 types, is_valid will return False

        :return: bool
        """

        return ".zip" in self.url_name or "[To Parent Directory]" == self.url_name or self.url_name == "ActivePerim"

    def __str__(self):
        if id != -1:
            return f"Fire Event {self.fire_id}: {self.url_name} in year {self.year}, state {self.state}"
        return f"Fire Event Unknown: {self.url_name} in year {self.year}, state {self.state}"

    def to_url(self) -> str:
        """
        Converts a FireEvent object into the url
        :return: url. e.g. "https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2017_fire_data/California/Eclipse"
        """
        # although there might be time zone difference, we only take the year part so it is not a big issue.
        current_year = datetime.datetime.now().date().year
        year_str = "current_year" if self.year == current_year else str(self.year)
        return f"{FireCrawler.BASE_DIR}{year_str}_fire_data/{self.state}/{self.url_name}"

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts a FireEvent object into a dictionary.
        :return: Dict[str, Any]
            e.g. {"year": 2017,
                "firename": "Sand",
                "state": "California",
                "id": 299,
                "url":"https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/...."}
        """
        return {"year": self.year,
                "firename": self.url_name,
                "state": self.state,
                "id": self.fire_id,
                "url": self.to_url()}

    def to_tuple(self, new_id) -> Tuple[int, int, str, str]:
        self.fire_id = new_id if self.fire_id == -1 else self.fire_id
        return self.fire_id, self.year, self.state, self.url_name


class FireCrawler(CrawlerBase):
    # BASE_DIR is the website directory the crawler will crawl
    BASE_DIR = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
    RE_EXTRACT_FIRE_EVENTS_IN_STATE = re.compile(r'<A .*?>(.*?)</A>', re.S | re.M)
    RE_EXTRACT_ALL_FIRES = re.compile(r'<A .*?>(\w*?)</A>', re.S | re.M)
    RE_EXTRACT_FILES_IN_FIRE_EVENTS = re.compile(r'<A .*?>([a-z]{2}_.+?)</A>', re.S | re.M)

    def __init__(self, states: List[str]):
        """
        Initialization for the crawler.
        :param states: list of states that the crawler needs to crawl, case-insensitive.
                e.g. ["California", "Nevada"]
        """
        super().__init__()
        self.states = [state.capitalize() for state in states]
        # states is a list of states that the crawler needs to crawl
        FireCrawler._cleanup()
        # empty the folder first to create a clean environment for fire record files

    @staticmethod
    @retry(stop_max_attempt_number=3)
    def _get_url(url: str, page_name: str) -> str:
        """
        Helper function for request.get().
        When request.get() meets the connection error, it will retry.
        If retry fails for 5 attempts, it will throw RuntimeError.
        :param url: str,
                e.g. 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
        :param page_name: str,
                e.g. 'main_page'
        :return: str,
                e.g. the string of all HTML code from 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
        """
        logger.info(f"Fetching {page_name} page ...")
        response = requests.get(url).content.decode("utf-8")
        logger.info(f"Finished fetching {page_name} page.")
        return response

    @staticmethod
    @retry(stop_max_attempt_number=3)
    def _download_single_file(url: str, file: str, out_path: str) -> None:
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
                e.g. [FireEvent(-1, 2015, 'California', 'FireA'), FireEvent(-1, 2015, 'California', 'FireB')]
        """
        logger.info(f"Fetching fire events in {state} in year {year}.")
        # although there might be time zone difference, we only take the year part so it is not a big issue.
        current_year = datetime.datetime.now().date().year
        url_year = "current_year" if current_year == year else year
        fire_events_page_in_state = FireCrawler._get_url(f"{FireCrawler.BASE_DIR}{url_year}_fire_data/{state}",
                                                         f"{state} State of year {year}")
        fire_names_in_this_state = FireCrawler.RE_EXTRACT_FIRE_EVENTS_IN_STATE.findall(fire_events_page_in_state)
        logger.info(f"Finished fetching fire events in {state} in year {year}.")
        return list(map(lambda single_fire_name: FireEvent(year, state, single_fire_name), fire_names_in_this_state))

    @staticmethod
    def _filter_out_invalid_fire_events(fires: List[FireEvent]) -> None:
        """
        Find those invalid FireEvent objects and remove them from the input list
        :param fires: list of FireEvent objects.
                e.g. [FireEvent(-1, 2015, 'California', 'FireA'), FireEvent(-1, 2015, 'California', 'FireB')]
        """
        for fire_event in fires[:]:
            if fire_event.is_invalid():
                fires.remove(fire_event)

    def extract_all_fires(self, start_year: int) -> List[FireEvent]:
        """
        Extracts all fires on the website and return.
        The returned value is a list of tuples:(year:int, state:string, fire's name in its url)
        :param start_year: int, start year for the crawler. Record before the start year will be deleted.
                e.g. 2015
        :return: list of FireEvent objects
                e.g. [FireEvent(-1, 2015, 'California', 'FireA'), FireEvent(-1, 2015, 'California', 'FireB')]
        """
        logger.info("Attempting to get all links...")
        current_year = datetime.datetime.now().date().year
        # fetch all year nodes from the website, may encounter errors
        # add a try-except block, and while loop to keep trying
        # if attempts > 3 raise an exception
        try:
            main_page = self._get_url(FireCrawler.BASE_DIR, "main_page")
        except requests.exceptions.RequestException:
            logger.error("Error: Cannot fetch main_page in function extract_all_fires()")
            raise FireCrawlException("Error: Cannot fetch main_page in function extract_all_fires")
            # retry exception
        else:
            # the last node is "historical_fire_data" and we don't want it
            each_year_sub_links = FireCrawler.RE_EXTRACT_ALL_FIRES.findall(main_page)[:-1]
            # sub_links_of_each_year are now fire data of a certain year or current year
            # e.g. '2010_fire_data', 'current_year_fire_data'
            fires: List = []
            for each_year_sub_link in each_year_sub_links:
                # sub_link_of_each_year: e.g. '2010_fire_data'
                # to change "current_year" to the real year as an integer
                year_as_int = current_year if each_year_sub_link == "current_year_fire_data" \
                    else int(each_year_sub_link.split("_")[0])
                # ignore years that before the start year
                # filter out links that is too old
                if year_as_int >= start_year:
                    for state in self.states:
                        # for each state, extract fire events in that year at that state
                        fires.extend(self._extract_fire_events_in_state(year_as_int, state))
            # call helper function to filter out invalid fire events
            self._filter_out_invalid_fire_events(fires)
            return fires

    @staticmethod
    def _download_fire_record(single_file_name: str, used_folder_names: Set[str], url_of_fire_event: str) -> None:
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
        else:
            logger.info(f"Skipping downloading useless zip file {single_file_name}")

    @staticmethod
    @retry(retry_on_exception=requests.exceptions.RequestException, stop_max_attempt_number=3)
    def _extract_file_names_in_fire_event(url_of_fire_event: str) -> List[str]:
        """
        Extracts all file names from a fire_event page. Return a list of all file names.
        :param url_of_fire_event: the url of the fire_event
                e.g. https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2017_fire_data/California/Antelope/
        :return: e.g. ["ca_antelope_20170706_1930_dd83.CPG", "ca_antelope_20170706_1930_dd83.dbf"]
        """
        fire_page = FireCrawler._get_url(url_of_fire_event, url_of_fire_event)
        return FireCrawler.RE_EXTRACT_FILES_IN_FIRE_EVENTS.findall(fire_page)

    @staticmethod
    def _extract_one_folder(abs_path: str, is_sequential: bool, fire_id: int, state: str) -> Dict[str, str]:
        """
        Calls fire extractor and extracts one fire_record
        :param abs_path: str, name of the folder
                e.g. "C:\myResearch\Wildfires\data\fire-data\ca_saddle_ridge_20191011_1014_dd83"
        :param is_sequential: bool, if this fire is a part of a sequence of fire
        :param fire_id: int
                    e.g. 700
        :param state: str
                    e.g. "California"
        :return: dict of all information in the record
                    e.g. {'year': 2019, 'firename': 'TRESTLE', 'agency': 'USFS', 'datetime':
                    datetime.datetime(2019, 6, 5, 12, 0), 'area': 0.538906158705, 'geopolygon_full': ....}
        """
        # extract the shapefile into a dictionary called single_record
        try:
            single_record = FireExtractor.extract(abs_path, is_sequential, fire_id, state)
        except IncompleteShapefileError as err:
            # the extractor result can be empty when the record is incomplete and cannot be decoded
            # in this situation, skip the record
            logger.warning(str(err))
            return dict()
        return single_record

    @staticmethod
    def _extract_all_folders(fire_id: int, state: str) -> List[Dict[str, Any]]:
        """
        Extracts all folders associated with a fire event.
        :param fire_id: int
                e.g. 700
        :param state: str
                e.g. "California"
        :return: a list of dictionaries of all information in the event
                e.g. e.g. [{'year': 2019, 'firename': 'TRESTLE', 'agency': 'USFS', 'datetime':
                    datetime.datetime(2019, 6, 5, 12, 0), 'area': 0.538906158705, 'geopolygon_full': ....}, {...}]
        """
        all_folder_names = glob.glob(os.path.join(FIRE_DATA_DIR, "[a-z]*"))
        # if the temporary directory has more than one sub directory(records), then the fire is a sequence of fire
        is_sequential = False if len(all_folder_names) == 1 else True
        list_of_extracted_records = [FireCrawler._extract_one_folder(record, is_sequential, fire_id, state)
                                     for record in all_folder_names]
        return list_of_extracted_records

    def crawl(self, url_of_fire_event: str, fire_id: int, state: str) -> List[Dict[str, Any]]:
        """
        Takes the url string of one fire and start to crawl all files. And then return a list of extracted fire records
        :param url_of_fire_event: str
                e.g. "https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/2016_fire_data/California/Happy_Camp"
        :param fire_id: int
                e.g. 201
        :param state: str
                e.g. "California"
        """
        # get all folder names under the data folder
        used_folder_names = set(os.path.split(folder)[1] for folder in glob.glob(os.path.join(FIRE_DATA_DIR, "[a-z]*")))
        # grab all fire names in the page
        # for loop for runtime error
        # download useful files
        for file in FireCrawler._extract_file_names_in_fire_event(url_of_fire_event):
            self._download_fire_record(file, used_folder_names, url_of_fire_event)
        list_of_records = FireCrawler._extract_all_folders(fire_id, state)
        # delete all downloaded temporary directories
        FireCrawler._cleanup()
        return list_of_records

    @staticmethod
    def _cleanup() -> None:
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
    # print(list(map(lambda fire: str(fire), test_crawler.extract_all_fires(2015))))
    # used = set()
    # test_crawler.cleanup()
    # fire_list = test_crawler.extract_all_fires()
    # random_number = random.randint(0, len(fire_list))
    # random_entry = fire_list[random_number]
    # random_url = test_crawler.generate_url_from_tuple(random_entry[0], random_entry[1],random_entry[2], 2019)
    # test_crawler.crawl(random_url)

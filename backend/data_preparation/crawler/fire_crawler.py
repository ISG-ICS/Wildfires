import re
import requests
import rootpath
import wget
import os
import datetime
import logging
import shutil
import urllib
import random
from typing import List
rootpath.append()

from paths import FIRE_DATA_DIR
from backend.data_preparation.crawler.crawlerbase import CrawlerBase

logger = logging.getLogger('TaskManager')


class FireCrawler(CrawlerBase):

    def __init__(self, states: List[str]):
        """
        Initialization for the crawler.
        :param states: list of states that the crawler needs to crawl
        """
        super().__init__()
        self.baseDir = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
        # baseDir is the website directory the crawler will crawl
        self.states = states
        # states is a list of states that the crawler needs to crawl

    # self.start() is removed because it is removed from the crawler base

    @staticmethod
    def get_url(url: str, page_name: str, function_name: str, max_attempts=10,) -> str:
        """
        Helper function for request.get().
        Handles connection errors.
        :param url: str
        :param page_name: str
        :param function_name: str
        :param max_attempts: int
        :return: str
        """
        for attempt in range(max_attempts):
            try:
                response = requests.get(url).content.decode("utf-8")
            except requests.exceptions.RequestException:
                logger.info(f"Cannot fetch {page_name} page in function {function_name}")
                logger.info(f"Attempting a second time... Remaining attempts:{10 - attempt}")
            else:
                break
        else:
            logger.error(f"Failed to fetch {page_name} page in function {function_name}")
            raise RuntimeError(f"Too many failed attempts in fetching {page_name} page in function {function_name}")
        return response

    def extract_all_fires(self) -> List[tuple]:
        """
        Extract all fires on the website and return.
        The returned value is a list of tuples:(year:int, state:string, fire's name in its url)
        :return: list of tuples
        """
        current_year = datetime.datetime.now().date().year
        # fetch all year nodes from the website, may encounter errors
        # add a try-except block, and while loop to keep trying
        # if attempts > 10 raise an exception
        main_page = self.get_url(self.baseDir, "main_page", "extract_all_fires()", 10)
        re_formula = r'<A .*?>(\w*?)</A>'
        year_nodes = re.findall(re_formula, main_page, re.S | re.M)[:-1]
        # year_nodes are now fire data of a certain year or current year
        # e.g. '2010_fire_data', 'current_year_fire_data'
        fires = []
        for year_node in year_nodes:
            true_year = current_year if year_node == "current_year_fire_data" else int(year_node.split("_")[0])
            # to change "current_year" to the real year as an integer
            for state in self.states:
                # try except for network errors
                list_of_state_fires = self.get_url(f"{self.baseDir}{year_node}/{state}",
                                                   f"{state} State of year {year_node}",
                                                   "extract_all_fires()", 10)
                # crawl the all fires in this state
                re_formula = r'<A .*?>(.*?)</A>'
                # This re_formula is different from the one used
                firenames = re.findall(re_formula, list_of_state_fires, re.S | re.M)
                fires.extend((map(lambda f: (true_year, state, f),firenames)))
        # to delete exceptions: "[To Parent Directory]" "whatever.zip"
        # ActivePerim is an useless link which contains metadata over the year, existing in links before 2016 Skip it
        for year, state, firename in fires[:]:
            if "." in firename or "[To Parent Directory]" == firename or firename == "ActivePerim":
                fires.remove((year, state, firename))
        return fires

    @staticmethod
    def generate_url_from_tuple(tuple_year: int, tuple_state: str, tuple_firename: str, current_year: int) -> str:
        """
        Take year, state, and url name and convert the entry to the url
        :param tuple_year: int
        :param tuple_state: str
        :param tuple_firename: str
        :param current_year: int
        :return: str
        """
        baseDir = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
        year_str = "current_year" if tuple_year == current_year else str(tuple_year)
        url = f"{baseDir}{year_str}_fire_data/{tuple_state}/{tuple_firename}"
        return url

    def crawl(self, url_to_crawl):
        """
        Takes the url string of one fire and start to crawl all files
        :param url_to_crawl: str
        :return: None
        """
        used_folder_names = set()
        # grab all firenames in the page
        # for loop for runtime error
        fire_page = self.get_url(url_to_crawl, url_to_crawl, "crawl()", 10)
        res = r'<A .*?>(ca_.+?)</A>'
        filenames = re.findall(res, fire_page, re.S | re.M)
        # download useful files
        for file in filenames:
            if not ".zip" == file[-4:]:
                # if it is a zip don't download
                folder_name = file.split(".")[0]
                if folder_name not in used_folder_names:
                    used_folder_names.add(folder_name)
                    os.makedirs(os.path.join(FIRE_DATA_DIR,folder_name))
                    # os.makedirs(FIRE_DATA_DIR + "/" + folder_name)
                outpath = os.path.join(FIRE_DATA_DIR, folder_name)
                # outpath = FIRE_DATA_DIR + "/" + folder_name + "/"
                for attempts in range(10):
                    try:
                        wget.download(url=url_to_crawl + "/" + file, out=outpath)
                    except urllib.error.URLError:
                        logger.warning(f"Cannot download {url_to_crawl} in crawl()")
                        logger.warning(f"Attempting a second time... Remaining attempts:{10 - attempts}")
                    else:
                        break
                else:
                    logger.error(f"Cannot download {url_to_crawl} in crawl(), max attempts reached")
                    raise RuntimeError("Cannot download {url_to_crawl} in crawl()")
        return

    @staticmethod
    def cleanup():
        """
        Clean up the temp data folder
        :return:
        """
        folders_to_remove = [os.path.join(FIRE_DATA_DIR, f) for f in os.listdir(FIRE_DATA_DIR)]
        for folder_name in folders_to_remove:
            if folder_name.__contains__(".DS"):
                continue
            shutil.rmtree(folder_name)


if __name__ == '__main__':
    # module tester
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    test_crawler = FireCrawler(["California"])
    fire_list = test_crawler.extract_all_fires()
    random_number = random.randint(0, len(fire_list))
    random_entry = fire_list[random_number]
    random_url = test_crawler.generate_url_from_tuple(random_entry[0], random_entry[1],random_entry[2], 2019)
    test_crawler.crawl(random_url)

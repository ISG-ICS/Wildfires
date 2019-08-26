import re
import requests
import rootpath
import wget
import os
import datetime
import logging
import shutil
import urllib
rootpath.append()

from paths import FIRE_DATA_DIR
from backend.data_preparation.crawler.crawlerbase import CrawlerBase

logger = logging.getLogger('TaskManager')


class FireCrawler(CrawlerBase):

    def __init__(self, states):
        """
        Initialization for the crawler.
        :param states: list of states that the crawler needs to crawl
        """
        super().__init__()
        self.baseDir = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
        self.years = []
        self.states = states

    def start(self):
        """
        Start the crawler, not used.
        Keep it here to satisfy crawlerbase abstract method.
        :return:
        """
        return

    def extract_all_fires(self):
        """
        Extract all fires on the website and return.
        The returned value is a list of tuples:(year:int, state:string, fire's name in its url)
        :return: list of tuples
        """
        current_year = datetime.datetime.now().date().year
        main_page = requests.get(url=self.baseDir).content.decode("utf-8")
        re_formula = r'<A .*?>(\w*?)</A>'
        year_nodes = re.findall(re_formula, main_page, re.S | re.M)[:-1]
        # year_nodes are now fire data of a certain year or current year
        # e.g. '2010_fire_data', 'current_year_fire_data'
        fire = []
        for year_node in year_nodes:
            true_year = current_year if year_node == "current_year_fire_data" else int(year_node.split("_")[0])
            # to change "current_year" to the real year as an integer
            for state in self.states:
                list_of_state_fires = requests.get(url=f"{self.baseDir}{year_node}/{state}").content.decode("utf-8")
                # crawl the all fires in this state
                re_formula = r'<A .*?>(.*?)</A>'
                fires = re.findall(re_formula, list_of_state_fires, re.S | re.M)
                fire += list(map(lambda f: (true_year, state, f), fires))
        # to delete exceptions: "[To Parent Directory]" "whatever.zip"
        for i in fire[:]:
            if "." in i[2] or "[To Parent Directory]" == i[2]:
                fire.remove(i)
        return fire

    def generate_url_from_tuple(self, year_of_t, state_of_t, name_of_t, current_year):
        """
        Take year, state, and url name and convert the entry to the url
        :param year_of_t: int
        :param state_of_t: str
        :param name_of_t: str
        :param current_year: int
        :return: str
        """
        yearstring = "current_year" if year_of_t == current_year else str(year_of_t)
        url = f"{self.baseDir}{yearstring}_fire_data/{state_of_t}/{name_of_t}"
        return url

    def crawl(self, url_to_crawl):
        """
        Takes the url string of one fire and start to crawl all files
        :param url_to_crawl: str
        :return: none
        """
        if "ActivePerim" in url_to_crawl:
            return
        # ActivePerim is useless link which contains metadata over the year, existing in links before 2016 Skip it
        used_folder_names = set()
        # grab all firenames in the page
        fire_page = requests.get(url=url_to_crawl).content.decode("utf-8")
        res = r'<A .*?>(ca_.+?)</A>'
        filenames = re.findall(res, fire_page, re.S | re.M)
        # download useful files
        for f in filenames:
            if ".zip" == f[-4:]:
                # if it is a zip don't download
                continue
            else:
                foldername = f.split(".")[0]
                if not foldername in used_folder_names:
                    used_folder_names.add(foldername)
                    os.makedirs(FIRE_DATA_DIR + "/" + foldername)
                outpath = FIRE_DATA_DIR + "/" + foldername + "/"
                while True:
                    try:
                        wget.download(url=url_to_crawl + "/" + f, out=outpath)
                    except urllib.error.URLError:
                        continue
                    break
        return

    def cleanup(self):
        """
        Clean up the temp data folder
        :return:
        """
        foldersToRemove = [os.path.join(FIRE_DATA_DIR, f) for f in os.listdir(FIRE_DATA_DIR)]
        for f in foldersToRemove:
            if f.__contains__(".DS"):
                continue
            shutil.rmtree(f)

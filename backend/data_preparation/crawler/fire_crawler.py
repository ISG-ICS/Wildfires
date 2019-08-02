from zipfile import ZipFile
import re
import requests
import rootpath
import wget
import os
import datetime
import shutil
rootpath.append()

from paths import FIRE_DATA_DIR
from backend.data_preparation.crawler.crawlerbase import CrawlerBase


class FireCrawler(CrawlerBase):
    """
             @          Layer 0
        / /  |  \  \
        1 2  3  4  c    Layer 1
        | |  |  |  |
        C C  C  C  C    Layer 2(determined)
        /\/\ /\ /\ /\
       f ffff ff ff f   Nodes

    Step 1: Get Layer 1: Layer 1 pattern: year_fire_data, current_fire_data
            add the absolute link into to_check
    Step 2: Get Nodes: Nodes pattern: fire_name

    """
    def __init__(self):
        super().__init__()
        self.baseDir = 'https://rmgsc.cr.usgs.gov/outgoing/GeoMAC/'
        self.years = []
        self.explored_year = set()
        self.explored_fire = set()
        self.to_check = []

    def start(self):
        """
        Start the crawler
        :return:
        """

    def extract_all_fires(self):
        """
        extract all fires on the website and return :
        tuples of (trueyear,firename)
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
            list_of_CA_fires = requests.get(url="{}{}/California/".format(self.baseDir, year_node)).content.decode("utf-8")
            re_formula = r'<A .*?>(\w*?)</A>'
            fires = re.findall(re_formula, list_of_CA_fires, re.S | re.M)
            fire += list(map(lambda f: (true_year, f), fires))
        return fire

    def generate_url_from_tuple(self, fires:set, current_year:int):
        urls = []
        for t in fires:
            year_of_t = "current_year" if t[0] == current_year else str(t[0])
            urls.append("{}{}_fire_data/California/{}".format(self.baseDir, year_of_t, t[1]))
        return urls

    def crawl(self, url_to_crawl):
        """
        takes the url string of one fire and start to crawl all files
        :param url_to_crawl: str
        :return: none
        """
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
                    print("Downloading: {}...".format(foldername))
                outpath = FIRE_DATA_DIR + "/" + foldername + "/"
                wget.download(url=url_to_crawl + "/" + f, out=outpath)
        return

    def cleanup(self):
        """
        clean up the temp data folder
        Haven't been test yet since I don't know what right the runnable have
        on the server
        :return:
        """
        print("Cleaning up the temp folder...")
        foldersToRemove = [os.path.join(FIRE_DATA_DIR, f) for f in os.listdir(FIRE_DATA_DIR)]
        for f in foldersToRemove:
            if f.__contains__(".DS"):
                continue
            shutil.rmtree(f)

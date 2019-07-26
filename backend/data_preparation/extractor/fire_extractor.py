import rootpath
rootpath.append()
from backend.data_preparation.extractor.extractorbase import ExtractorBase
from paths import FIRE_DATA_DIR
from typing import Dict
import shapefile
import datetime

class FireExtractor(ExtractorBase):
    def __init__(self):
        super().__init__()



    def extract(self, path, folder):
        """
        extract data from file to dict
        :param sf:
        :return:
        """
        data =[]
        shp = shapefile.Reader(path + "/" + folder)
        firetime = datetime.datetime.strptime(shp.records()[0]['perDatTime'], '%m/%d/%Y %I:%M:%S %p')
        firename = shp.records()[0]['fireName'].capitalize()
        firepolygon_x








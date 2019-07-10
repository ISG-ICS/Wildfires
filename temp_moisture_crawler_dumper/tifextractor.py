import json
import os
from typing import Dict

from osgeo import gdal

from backend.data_preparation.extractor.extractorbase import ExtractorBase

class TIFExtractor(ExtractorBase):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.tif = gdal.Open(filename)
        self.data: Dict = dict()

    def extract(self):
        gt = self.tif.GetGeoTransform()
        x_min = gt[0]
        x_size = gt[1]
        y_min = gt[3]
        y_size = gt[5]
        im_width = self.tif.RasterXSize
        im_height = self.tif.RasterYSize
        ulx = x_min  # upper left x
        uly = y_min  # upper left y
        lrx = im_width * x_size + x_min  # lower right x
        lry = im_height * y_size + y_min  # lower right y
        ds = gdal.Translate('output.xyz', self.tif, projWin=[ulx, uly, lrx, lry])

        dictionary = dict()  # creates a new dictionary to store data

        xyzFile = open('output.xyz')
        line = xyzFile.readline()
        while line:
            long = line.split()[0]
            lat = line.split()[1]
            value = line.split()[2]
            if str(value) != '-999000000':
                if 't.full' in self.filename:  # for historical temperature data
                    time = self.filename[self.filename.find('month_')+6:self.filename.find('.tif')]
                    dictionary[(lat, long, time)] = value
                if 'w.full' in self.filename:  # for historical moisture data
                    time = self.filename[self.filename.find('full.')+5:self.filename.find('.tif')]
                    dictionary[(lat, long, time)] = value
            line = xyzFile.readline()

        self.data: Dict = dictionary
        os.remove('output.xyz')
        return self.data

    def export(self, file_type: str, file_name) -> None:  # json
        if file_type == 'json':
            json.dump(self.data, open(file_name, 'w'))
        # TODO: support other file format like CSV

    def __getitem__(self, lat_lng_pair: tuple) -> float:
        return self.data.get(str(lat_lng_pair))


if __name__ == '__main__':
    tif_extractor = TIFExtractor('w.full.20190519.tif')
    dict = tif_extractor.extract()
    print(dict)

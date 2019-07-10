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

    def extract_data_from_geotif(self, tif):
        gt = self.tif.GetGeoTransform()  # get the attributes of the tif file
        # select the attributes needed
        x_min = gt[0]  # the x of the top left point
        x_size = gt[1]  # each x contains how many pixels
        y_min = gt[3]  # the y of the top left point
        y_size = gt[5]  # each y contains how many pixels

        im_width = self.tif.RasterXSize  # the width of the array
        im_height = self.tif.RasterYSize  # the height of the array
        ulx = x_min  # upper left x
        uly = y_min  # upper left y
        lrx = im_width * x_size + x_min  # lower right x
        lry = im_height * y_size + y_min  # lower right y

        # calculate the tif file's data and output it into 'output.xyz'
        # 'output.xyz' file will be deleted later, don't need to worry
        ds = gdal.Translate('output.xyz', self.tif, projWin=[ulx, uly, lrx, lry])

    def extract(self):
        self.extract_data_from_geotif(self.tif)

        dictionary = dict()  # creates a new dictionary to store data
        xyzFile = open('output.xyz')
        line = xyzFile.readline()
        while line:  # get dictionary from the xyzfile
            long, lat, value = self.get_long_lat_value(line)
            if str(value) != '-999000000':  # ignore the invalid value
                if 't.full' in self.filename:  # for historical temperature data
                    # get time from file's name
                    time = self.filename[self.filename.find('month_')+6:self.filename.find('.tif')]
                    # put the data into the dictionary
                    dictionary[(lat, long, time)] = value
                if 'w.full' in self.filename:  # for historical moisture data
                    time = self.filename[self.filename.find('full.')+5:self.filename.find('.tif')]
                    dictionary[(lat, long, time)] = value
            line = xyzFile.readline()

        self.data: Dict = dictionary
        os.remove('output.xyz')
        return self.data

    def get_long_lat_value(self, line):
        long = line.split()[0]
        lat = line.split()[1]
        value = line.split()[2]
        return long, lat, value

    def export(self, file_type: str, file_name) -> None:  # json
        if file_type == 'json':
            json.dump(self.data, open(file_name, 'w'))
        # TODO: support other file format like CSV

    def __getitem__(self, lat_lng_pair: tuple) -> float:
        return self.data.get(str(lat_lng_pair))


if __name__ == '__main__':
    # use case of TIFExtractor, put in the path to the tif file
    tif_extractor = TIFExtractor('w.full.20190519.tif')
    # using tif extractor to get the dictionary, which is (lat,long,time):value
    dict = tif_extractor.extract()
    print(dict)

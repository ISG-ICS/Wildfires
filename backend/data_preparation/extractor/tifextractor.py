import json
import os
from typing import Dict

# from osgeo import gdal
from raster2xyz.raster2xyz import Raster2xyz

from backend.data_preparation.extractor.extractorbase import ExtractorBase


class TIFExtractor(ExtractorBase):
    def __init__(self, filename: str):
        super().__init__(filename)
        # self.tif = gdal.Open(filename)
        self.tif = filename
        self.data: Dict = dict()

    def extract(self):
        self.extract_data_from_geotif()

        dictionary = dict()  # creates a new dictionary to store data
        xyzFile = open('output.xyz')
        line = xyzFile.readline()
        flag = 0  # to skip the first line 'x,y,z'
        while line:  # get dictionary from the xyzfile
            if flag == 0:
                flag = 1
                line = xyzFile.readline()
                continue
            lat, long_, value = self.get_lat_long_value(line)
            if str(value) != '-999000000.0':  # ignore the invalid value
                time = self.get_time_from_filename()
                dictionary[(lat, long_, time)] = value
            line = xyzFile.readline()

        self.data: Dict = dictionary
        os.remove('output.xyz')
        return self.data

    def extract_data_from_geotif(self):
        # if the gdal package is going to be used
        # gt = self.tif.GetGeoTransform()  # get the attributes of the tif file
        # # select the attributes needed
        # x_min = gt[0]  # the x of the top left point
        # x_size = gt[1]  # each x contains how many pixels
        # y_min = gt[3]  # the y of the top left point
        # y_size = gt[5]  # each y contains how many pixels
        #
        # im_width = self.tif.RasterXSize  # the width of the array
        # im_height = self.tif.RasterYSize  # the height of the array
        # ulx = x_min  # upper left x
        # uly = y_min  # upper left y
        # lrx = im_width * x_size + x_min  # lower right x
        # lry = im_height * y_size + y_min  # lower right y
        #
        # # calculate the tif file's data and output it into 'output.xyz'
        # # 'output.xyz' file will be deleted later, don't need to worry
        # ds = gdal.Translate('output.xyz', self.tif, projWin=[ulx, uly, lrx, lry])

        rtxyz = Raster2xyz()
        out_csv = 'output.xyz'
        rtxyz.translate(self.tif, out_csv)

    def get_lat_long_value(self, line):
        long_, lat, value = line.split(',')
        value = value.strip('\n')
        return lat, long_, value

    def get_time_from_filename(self):
        # sample filename: t.full.1stday_month_20130611.tif, w.full.20190519.tif
        time = self.tif.split('.')[-2].split('_')[-1]
        return time

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
    dictionary = tif_extractor.extract()
    print(dictionary)

import pygrib

from osgeo import gdal


class GRIBExtractor:
    def __init__(self, open_file_name, prop_name, prop_typeOfLevel='surface', prop_first=0, prop_second=10):
        self.file_handler = pygrib.open(open_file_name)
        self.prop_name = prop_name
        self.prop_typeOfLevel = prop_typeOfLevel
        self.prop_first = prop_first
        self.prop_second = prop_second

    def extractMoisture(self):
        prop_msg = self.file_handler.select(name=self.prop_name, scaledValueOfFirstFixedSurface=self.prop_first,
                                            scaledValueOfSecondFixedSurface=self.prop_second)[0]
        prop_dict = dict()  # creates a new dictionary to store data
        prop_vals = prop_msg.values  # values under the started property
        lats, lons = prop_msg.latlons()
        for row_cnt in range(0, len(prop_vals)):
            for col_cnt in range(0, len(prop_vals[row_cnt])):
                prop_dict[str((lats[row_cnt][col_cnt], lons[row_cnt][col_cnt]))] = prop_vals[row_cnt][col_cnt]
        return prop_dict  # the location coordinates are different, don't need to worry about duplicated keys

    def extractTemperatrue(self):
        prop_msg = self.file_handler.select(name=self.prop_name, typeOfLevel=self.prop_typeOfLevel)[0]
        prop_dict = dict()  # creates a new dictionary to store data
        prop_vals = prop_msg.values  # values under the started property
        lats, lons = prop_msg.latlons()
        for row_cnt in range(0, len(prop_vals)):
            for col_cnt in range(0, len(prop_vals[row_cnt])):
                prop_dict[str((lats[row_cnt][col_cnt], lons[row_cnt][col_cnt]))] = prop_vals[row_cnt][col_cnt]
        return prop_dict  # the location coordinates are different, don't need to worry about duplicated key


class TIFExtractor:
    def __init__(self, open_file_name):
        self.tif = gdal.Open(open_file_name)

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


if __name__ == '__main__':
    # exp = pygrib.open('moisture_data/cdas1.t00z.sfluxgrbf02.grib2.txt').read()
    # for line in exp:
    #     print(line)
    # file = pygrib.open('moisture_data/cdas1.t00z.sfluxgrbf02.grib2.txt')
    exp = TIFExtractor('historical_temperature_data/t.full.1stday_month_20140820.tif')
    exp.extract()

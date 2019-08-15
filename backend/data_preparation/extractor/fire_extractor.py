import rootpath
rootpath.append()
import re
from backend.data_preparation.extractor.extractorbase import ExtractorBase
import shapefile
import datetime
from shapely.geometry import shape
from shapely.geometry.multipolygon import MultiPolygon
class FireExtractor(ExtractorBase):
    def __init__(self):
        super().__init__()


    def extract(self, path, record, if_sequence, id, state):
        """
        Extract useful information of a fire from a path
        :param path: str, path of the files of this fire
        :param record: str, the name of this record(stage)
        :param if_sequence: bool, if the stage belongs to a sequence of fire
        :param id: int, id of the aggregated fire
        :return: result: dict, all values needed
        """
        # The original data is not clean, field names are different each year
        # this dictionary is for the extractor to get the exactly year's field names
        # fieldsbyyear = {2010:("FIRE_NAME", "DATE_", "TIME_", "AGENCY"),
        #                 2011:("FIRE_NAME", "DATE_", "TIME_", "AGENCY"),
        #                 2012:("FIRE_NAME", "DATE_", "TIME_", "AGENCY"),
        #                 2013:("FIRE_NAME", "DATE_", "TIME_", "AGENCY"),
        #                 2014:("FIRE_NAME", "DATE_", "TIME_", "AGENCY"),
        #                 2015:("FIRE_NAME", "DATE_", "TIME_", "AGENCY"),
        #                 2016:("fireName", "perDatTime", "agency"),
        #                 2017:("fireName", "perDatTime", "agency"),
        #                 2018:("fireName", "perDatTime", "agency"),
        #                 2019:("FIRENAME", "DATECRNT","AGENCY")}
        # extract the year number from record and convert it to an int
        try:
            year = int(re.search(r"\d{8}",record).group()[:4])
        except AttributeError:
            year = int(re.search(r"\d{7}",record).group()[:4])

        # defining fields each year in dict is not proper since
        # before 2016 there are 4 fields needed. But after 2016 there are only 3
        # decided to use if statement

        # NOTE: current year's schema is different from 2016-2018, not sure if it is a temp field names for
        # current_year only or the names of fields starts to change again after 2018

        # result to return -- a dict
        result = dict()

        try:
            shp = shapefile.Reader(path + "/" + record)
        except shapefile.ShapefileException:
            return result
        # print(shp.record(0))
        # fill result dict based on the format for this year
        if year < 2016:
            # FIRE_NAME, DATE_:  datetime.date(2014, 9, 11), TIME_: 0129, AGENCY: USFS or NULL
            result["firename"] = shp.record(0)["FIRE_NAME"].capitalize()
            result["agency"] = shp.record(0)["AGENCY"] if shp.record(0)["AGENCY"] != "" else "Unknown"
            try:
                result["datetime"] = datetime.datetime.strptime("{:%m%d%Y}".format(shp.record(0)["DATE_"]) + \
                                                            shp.record(0)['TIME_'], '%m%d%Y%H%M')
            except ValueError:
                result["datetime"] = datetime.datetime.strptime("{:%m%d%Y}".format(shp.record(0)["DATE_"] + datetime.timedelta(days=1)) + \
                                                                "0000", '%m%d%Y%H%M')
        else:
            try:
                result["firename"] = shp.record(0)["fireName"].capitalize()
                result["agency"] = shp.record(0)["agency"] if shp.record(0)["agency"] != "" else "Unknown"
                result["datetime"] = datetime.datetime.strptime(shp.record(0)['perDatTime'], '%m/%d/%Y %I:%M:%S %p') if \
                    len(shp.record(0)['perDatTime']) > 11 else datetime.datetime.strptime(shp.record(0)['perDatTime'], '%m/%d/%Y')
            except IndexError:
                result["firename"] = shp.record(0)["FIRENAME"].capitalize()
                result["agency"] = shp.record(0)["AGENCY"] if shp.record(0)["AGENCY"] != "" else "Unknown"
                result["datetime"] = datetime.datetime.strptime(shp.record(0)['PERDATTIME'], '%m/%d/%Y %I:%M:%S %p') if \
                    len(shp.record(0)['PERDATTIME']) > 11 else datetime.datetime.strptime(shp.record(0)['PERDATTIME'], '%m/%d/%Y')
        geom = self.extract_full_geom(shp)
        result["geopolygon_full"] = str(geom)
        result["geopolygon_large"] = str(self.simplify_multipolygon(geom,1.e-04))
        result["geopolygon_medium"] = str(self.simplify_multipolygon(geom,1.e-03))
        result["geopolygon_small"] = str(self.simplify_multipolygon(geom,1.e-02))
        result["year"] = year
        result["if_sequence"] = if_sequence
        result["id"] = id
        result["state"] = state
        return result

    def extract_full_geom(self, shp: shapefile.Reader):
        """
        Extract a full geom from a shp reader
        :param shp: shapefile.Reader
        :return: Multipolygon
        """
        fire = shp.shapeRecord(0).shape.__geo_interface__
        geom = shape(fire)
        return geom

    def simplify_multipolygon(self, multipolygon, threshold: float):
        """
        Simplify all components of a multipolygon
        :param multipolygon:shapely.geometry.Multipolygon
        :param threshold:float
        :return:shapely.geometry.Multipolygon
        """
        try:
            polygons = list(multipolygon)
        except TypeError:
            polygons = [multipolygon]
        for i in range(len(polygons)):
            polygons[i] = polygons[i].simplify(threshold)
        return MultiPolygon(polygons)


    def export(self, file_type: str, file_name: str):
        return




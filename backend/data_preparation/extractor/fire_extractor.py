import rootpath
rootpath.append()
import re
from backend.data_preparation.extractor.extractorbase import ExtractorBase
from paths import FIRE_DATA_DIR
from typing import Dict
import shapefile
import datetime

class FireExtractor(ExtractorBase):
    def __init__(self):
        super().__init__()


    def extract(self, path, record, if_sequence):
        """
        Extract useful information of a fire from a path
        :param path: str, path of the files of this fire
        :param record: str, the name of this record(stage)
        :param if_sequence: bool, if the stage belongs to a sequence of fire
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
        year = int(re.search(r"\d{8}",record).group()[:4])

        # defining fields each year in dict is not proper since
        # before 2016 there are 4 fields needed. But after 2016 there are only 3
        # decided to use if statement

        # NOTE: current year's schema is different from 2016-2018, not sure if it is a temp field names for
        # current_year only or the names of fields starts to change again after 2018

        # result to return -- a dict
        result = dict()

        # read the shp
        #!!!!record need to be fixed since some files are not the same name as their folders
        shp = shapefile.Reader(path + "/" + record)
        print(shp.record(0))
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
            if year < 2019:
                # fireName, perDatTime(maybe just date but no time), agency(might be null)
                result["firename"] = shp.record(0)["fireName"].capitalize()
                result["agency"] = shp.record(0)["agency"] if shp.record(0)["agency"] != "" else "Unknown"
                result["datetime"] = datetime.datetime.strptime(shp.record(0)['perDatTime'], '%m/%d/%Y %I:%M:%S %p') if \
                    len(shp.record(0)['perDatTime']) > 11 else datetime.datetime.strptime(shp.record(0)['perDatTime'], '%m/%d/%Y')
            else:
                # FIRENAME, DATECRNT, AGENCY
                result["firename"] = shp.record(0)["FIRENAME"].capitalize()
                result["agency"] = shp.record(0)["AGENCY"] if shp.record(0)["AGENCY"] != "" else "Unknown"
                result["datetime"] = datetime.datetime.strptime(shp.record(0)['DATECRNT'], '%m/%d/%Y %I:%M:%S %p') if \
                    len(shp.record(0)['DATECRNT']) > 11 else datetime.datetime.strptime(shp.record(0)['DATECRNT'], '%m/%d/%Y')

        #result["geopolygon"] = self.generate_geom_script(self.separate_multipart_shape(shp.shapeRecord(0).shape.points))
        result["geopolygon"] = shp.shapeRecord(0).shape.points
        result["year"] = year
        result["if_sequence"] = if_sequence
        print(result)
        return result

    def separate_multipart_shape(self,multipartshape):
        separated_shapes = []
        shown_points = set()
        current_shape = []
        for point in multipartshape:
            current_shape.append(point)
            if point in shown_points:
                print("endpoint:", point)
                separated_shapes.append(current_shape)
                current_shape = list()
                shown_points = set()
            shown_points.add(point)
        print(separated_shapes)
        return separated_shapes

    def generate_geom_script(self, separated_shapes):
        result = "MULTIPOLYGON("
        for shape in separated_shapes:
            result += "(("
            for point in shape:
                result += "{} {}, ".format(point[0],point[1])
            result = result[:-2] + ")),"
        print(result[:-1] + ")")
        return result[:-1] + ")"

    def export(self, file_type: str, file_name: str):
        return









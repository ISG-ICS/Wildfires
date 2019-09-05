"""
@author: Scarlett Zhang
This file contains 2 classes:
1. class IncompleteShapefileError: an Exception to be caught in pipeline main function.
2. class FireExtractor: the object of extractor from shapefile to dictionary with useful information
"""
import rootpath
rootpath.append()
import re
from backend.data_preparation.extractor.extractorbase import ExtractorBase
import shapefile
import logging
import datetime
from typing import Dict, List
from shapely.geometry import shape
from shapely.geometry.multipolygon import MultiPolygon

logger = logging.getLogger('TaskManager')


class IncompleteShapefileError(Exception):
    pass


class FireExtractor(ExtractorBase):

    def extract(self, path: str, record: str, if_sequence: bool, id: int, state: str) -> Dict[str, str]:
        """
        Reads a set of records and return the contents.
        This is a messy function since the data source is dirty.
        :param path: str, path of the folder
        :param record: str, name of the record
        :param if_sequence: bool, if this fire is a sequence of fire
        :param id: int
        :param state: str
        :return: dict of all information in the record
        """
        try:
            # get the year of this fire record
            year = int(re.search(r"\d{8}",record).group()[:4])
        except AttributeError:
            # there is a wrong formatted timestamp
            # sorry the data source is messy
            year = int(re.search(r"\d{7}",record).group()[:4])
        # defining fields each year in dict is not proper since
        # before 2016 there are 4 fields needed. But after 2016 there are only 3
        # decided to use if statement
        # NOTE: current year's schema is different from 2016-2018, not sure if it is a temp field names for
        # current_year only or the names of fields starts to change again after 2018
        # result to return -- a dict
        result = dict()
        # read the shapefile
        try:
            shp = shapefile.Reader(path + "/" + record)
        except shapefile.ShapefileException:
            # if the sub-files of the shapefile is not complete
            # then it is not a valid shapefile, and no result should be returned
            raise IncompleteShapefileError("Hit incomplete polygon files, skipping. ")
            # return result
        # fill result dict based on the format for this year
        if year < 2016:
            # FIRE_NAME, DATE_:  datetime.date(2014, 9, 11), TIME_: 0129, AGENCY: USFS or NULL
            result["firename"] = shp.record(0)["FIRE_NAME"].capitalize()
            # before 2016, record schema for firename is: FIRE_NAME
            result["agency"] = shp.record(0)["AGENCY"] if shp.record(0)["AGENCY"] != "" else "Unknown"
            # before 2016, record schema for agency is: AGENCY
            try:
                result["datetime"] = datetime.datetime.strptime("{:%m%d%Y}".format(shp.record(0)["DATE_"]) + shp.record\
                    (0).get('TIME_', "0000"), '%m%d%Y%H%M')
                # before 2016, record schema for datetime is: DATE_ and TIME_
            except ValueError:
                result["datetime"] = datetime.datetime.strptime("{:%m%d%Y}".format(shp.record(0)["DATE_"] + \
                    datetime.timedelta(days=1)) + "0000", '%m%d%Y%H%M')
                # sometimes, before 2016, record schema for datetime is: DATE_ ONLY, defaultly treated as fire
                # happened at 00:00
            try:
                #################hhhhhhh
                shp.record(0).get("A", shp.record(0).get("a"))
                result["area"] = float(shp.record(0)["ACRES"])
                # before 2016, record schema for area is: ACRES
            except IndexError:
                result["area"] = float(shp.record(0)["Acres"])
                # sometimes, before 2016, record schema for area is: Acres
        else:
            # after 2016
            try:
                result["firename"] = shp.record(0)["fireName"].capitalize()
                result["agency"] = shp.record(0)["agency"] if shp.record(0)["agency"] != "" else "Unknown"
                result["datetime"] = datetime.datetime.strptime(shp.record(0)['perDatTime'], '%m/%d/%Y %I:%M:%S %p') \
                if len(shp.record(0)['perDatTime']) > 11 else datetime.datetime.strptime(shp.record(0)['perDatTime'],
                                                                                         '%m/%d/%Y')
                # after 2016, record schema for firename is: fireName, for agency is: agency, for datetime is:
                # perDatTime, defaultly
            except IndexError:
                result["firename"] = shp.record(0)["FIRENAME"].capitalize()
                result["agency"] = shp.record(0)["AGENCY"] if shp.record(0)["AGENCY"] != "" else "Unknown"
                result["datetime"] = datetime.datetime.strptime(shp.record(0)['PERDATTIME'], '%m/%d/%Y %I:%M:%S %p') if \
                    len(shp.record(0)['PERDATTIME']) > 11 else datetime.datetime.strptime(shp.record(0)['PERDATTIME'],
                                                                                          '%m/%d/%Y')
                # For some records after 2016, record schema for firename is: FIRENAME, for agency is: AGENCY, for
                # datetime is: PERDATTIME
            try:
                result["area"] = float(shp.record(0)["GISACRES"])
                # after 2016, record schema for area is: GISACRES
            except IndexError:
                result["area"] = float(shp.record(0)["gisAcres"])
                # For some records after 2016, record schema for area is: gisAcres
        geom = self.extract_full_geom(shp)
        # basic geom is the full geom of this shapefile record
        # see function extract_full_geom below
        result["geopolygon_full"] = str(geom)
        # geopolygon_full is the full geom of this shapefile record
        result["geopolygon_large"] = str(self.simplify_multipolygon(geom,1.e-04))
        # geopolygon_large is the simpilfied full geom of this shapefile record, threshold is 1.e-04
        result["geopolygon_medium"] = str(self.simplify_multipolygon(geom,1.e-03))
        # geopolygon_medium is the simpilfied full geom of this shapefile record, threshold is 1.e-03
        result["geopolygon_small"] = str(self.simplify_multipolygon(geom,1.e-02))
        # geopolygon_small is the simpilfied full geom of this shapefile record, threshold is 1.e-02
        result["year"] = year
        # attribute "year" is the year extracted from record file names
        result["if_sequence"] = if_sequence
        # if_sequence is passed as a parameter. If in the temp folder, there are more than one set of records, then
        # if_sequence is True
        result["id"] = id
        # id is passed as a parameter
        result["state"] = state
        # state is passed as a parameter
        return result

    @staticmethod
    def extract_full_geom(shp: shapefile.Reader) -> MultiPolygon:
        """
        Extracts a full geom from a shp reader
        :param shp: shapefile.Reader
        :return: Multipolygon
        """
        fire = shp.shapeRecord(0).shape.__geo_interface__
        geom = shape(fire)
        return geom

    @staticmethod
    def simplify_multipolygon(multipolygon: MultiPolygon, threshold: float) -> MultiPolygon:
        """
        Simplifies all components of a multipolygon
        :param multipolygon:shapely.geometry.Multipolygon or shapely.geometry.polygon.Polygon
        :param threshold:float, the threshold of simplification
        :return:shapely.geometry.Multipolygon
        """
        try:
            # if polygon is a shapely.geometry.MultiPolygon, then it can be convert into a list of
            # shapely.geometry.Polygon
            polygons = list(multipolygon)
        except TypeError:
            # if multipolygon is a shapely.geometry.polygon.Polygon, need to explicitly convert into a list
            polygons = [multipolygon]
        for i in range(len(polygons)):
            # for each polygon in the list of polygons
            # simplify the polygon with object.simplify(tolerance, preserve_topology=True)
            # See https://shapely.readthedocs.io/en/stable/manual.html for more details
            polygons[i] = polygons[i].simplify(threshold)
        # merge polygons into a single multipolygon object and then return it
        return MultiPolygon(polygons)

    def export(self, file_type: str, file_name: str):
        """
        Useless function for this data pipeline. Keeps it here for abstractmethod
        :param file_type:
        :param file_name:
        :return:
        """
        return


if __name__ == '__main__':
    fe = FireExtractor()


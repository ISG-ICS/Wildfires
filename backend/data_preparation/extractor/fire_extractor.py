"""
@author: Scarlett Zhang
This file contains 2 classes:
1. class IncompleteShapefileError: an Exception to be caught in pipeline main function.
2. class FireExtractor: the object of extractor from shapefile to dictionary with useful information
"""
import rootpath
import re
from backend.data_preparation.extractor.extractorbase import ExtractorBase
import shapefile
import os
import logging
import datetime
from typing import Dict
from shapely.geometry import shape
from shapely.geometry.multipolygon import MultiPolygon

rootpath.append()

logger = logging.getLogger('TaskManager')


class IncompleteShapefileError(Exception):
    pass


class FireExtractor(ExtractorBase):
    # re expression to extract the year of the record from file names. Normally it is 8 consecutive digits
    RE_EXTRACT_YEAR_NORMAL = re.compile(r"\d{8}")
    # However, there are records with only 7 consecutive digits because of the carelessness of gov workers
    RE_EXTRACT_YEAR_ABNORMAL = re.compile(r"\d{7}")

    @staticmethod
    def _get_year(record: str) -> int:
        """
        Gets the year of the record.
        :param record: the name of the record.
                e.g. ca_airport_2_20190716_0940_dd83
        :return: year of this record
                e.g. 2019
        """
        # get the re expression to extract the year
        re_match_object_for_year = FireExtractor.RE_EXTRACT_YEAR_NORMAL.search(record)
        if re_match_object_for_year:
            # when it is normal (8 digits)
            return int(re_match_object_for_year.group()[:4])
        else:
            # when it is abnormal (7 digits)
            return int(FireExtractor.RE_EXTRACT_YEAR_ABNORMAL.search(record).group()[:4])

    @staticmethod
    def _get_datetime_before_2016(record: "shapefile._Record") -> datetime:
        """
        Gets the datetime of a certain record before 2016, record schema for datetime is: DATE_ and TIME_
        Sometimes there is only DATE_ but not TIME_
        :param record: the whole record of fire, shapefile._Record object.
                    e.g. Record['CA-LNU', 'JZR5', 'Wragg', datetime.date(2015, 8, 2), '0227', 'IR heat perimeter',
                    'State Agency', 'Y', '', '2015', datetime.date(2015, 8, 2), '', 'CA-LNU-006678', 8049.33]
        :return:datetime: e.g. 2015/08/02 02:27
        """
        return datetime.datetime.strptime("{:%m%d%Y}".format(record["DATE_"]) + record["TIME_"], '%m%d%Y%H%M')

    @staticmethod
    def _get_datetime_after_2016(record: "shapefile._Record") -> datetime:
        """
        Gets the datetime of a certain record after 2016, record schema for datetime is: PERDATTIME or perDatTime
        :param record: the whole record of fire, shapefile._Record object.
                    e.g. Record['CA-LNU', 'JZR5', 'Wragg', datetime.date(2015, 8, 2), '0227', 'IR heat perimeter',
                    'State Agency', 'Y', '', '2015', datetime.date(2015, 8, 2), '', 'CA-LNU-006678', 8049.33]
        :return:datetime: e.g. 2015/08/02 02:27
        """
        datetime_string = record.as_dict().get('PERDATTIME', record.as_dict().get('perDatTime'))
        datetime_object = (datetime.datetime.strptime(datetime_string, '%m/%d/%Y %I:%M:%S %p')
                           if len(datetime_string) > 11 else datetime.datetime.strptime(datetime_string, '%m/%d/%Y'))
        return datetime_object

    def extract(self, path: str, is_sequential: bool, fire_id: int, state: str) -> Dict[str, str]:
        """
        Reads a set of records and return the contents.
        This is a messy function since the data source is dirty.
        :param path: str, path of the folder
                e.g. "C:\myResearch\Wildfires\data\\fire-data\ca_trestle_20190605_1200_dd83"
        :param is_sequential: bool, if this fire is a part of a sequence of fire
        :param fire_id: int
                    e.g. 700
        :param state: str
                    e.g. "California"
        :return: dict of all information in the record
                    e.g. {'year': 2019, 'firename': 'TRESTLE', 'agency': 'USFS', 'datetime':
                    datetime.datetime(2019, 6, 5, 12, 0), 'area': 0.538906158705, 'geopolygon_full': ....}
        """
        logger.info(f"Extracting:{path}, fire_id: {fire_id}, state: {state}, is_sequential: {is_sequential}")
        # defining fields each year in dict is not proper since
        # before 2016 there are 4 fields needed. But after 2016 there are only 3
        # decided to use if statement
        # NOTE: current year's schema is different from 2016-2018, not sure if it is a temp field names for
        # current_year only or the names of fields starts to change again after 2018
        # result to return -- a dict
        data = dict()
        # record name is the name of the record folder
        record_name = os.path.basename(os.path.normpath(path))
        # get the year of the fire record
        # attribute "year" is the year extracted from record file names
        data['year'] = FireExtractor._get_year(record_name)
        # read the shapefile
        try:
            shapefile_reader = shapefile.Reader(os.path.join(path, record_name))
        except shapefile.ShapefileException:
            # if the sub-files of the shapefile is not complete
            # then it is not a valid shapefile, and no result should be returned
            raise IncompleteShapefileError("Hit incomplete polygon files, skipping. ")
        record = shapefile_reader.record(0)
        # fill result dict based on the format for this year
        if data['year'] < 2016:
            # FIRE_NAME, DATE_:  datetime.date(2014, 9, 11), TIME_: 0129, AGENCY: USFS or NULL
            # before 2016, record schema for firename is: FIRE_NAME
            data["firename"] = record["FIRE_NAME"].capitalize()
            # before 2016, record schema for agency is: AGENCY
            data["agency"] = record["AGENCY"] if record["AGENCY"] != "" else "Unknown"
            data["datetime"] = FireExtractor._get_datetime_before_2016(record)
            # before 2016, record schema for area is: ACRES
            # sometimes, before 2016, record schema for area is: Acres
            data["area"] = float(record.as_dict().get("ACRES", "Acres"))
        else:
            # after 2016
            # For some records after 2016, record schema for firename is: FIRENAME, for agency is: AGENCY, for
            # datetime is: PERDATTIME
            data["firename"] = record.as_dict().get("FIRE_NAME",  record.as_dict().get('fireName'))
            data["agency"] = record.as_dict().get("AGENCY", record.as_dict().get("agency")) \
                if record.as_dict().get("AGENCY", record.as_dict().get("agency")) != "" else "Unknown"
            data["datetime"] = FireExtractor._get_datetime_after_2016(record)
            # after 2016, record schema for area is: GISACRES
            # For some records after 2016, record schema for area is: gisAcres
            data["area"] = float(record.as_dict().get("GISACRES", record.as_dict().get("gisAcres")))
        geom = FireExtractor._extract_full_geom(shapefile_reader)
        # basic geom is the full geom of this shapefile record
        # see function extract_full_geom below
        data["geopolygon_full"] = str(geom)
        # geopolygon_full is the full geom of this shapefile record
        data["geopolygon_large"] = str(FireExtractor._simplify_multipolygon(geom,1.e-04))
        # geopolygon_large is the simplified full geom of this shapefile record, threshold is 1.e-04
        data["geopolygon_medium"] = str(FireExtractor._simplify_multipolygon(geom,1.e-03))
        # geopolygon_medium is the simplified full geom of this shapefile record, threshold is 1.e-03
        data["geopolygon_small"] = str(FireExtractor._simplify_multipolygon(geom,1.e-02))
        # geopolygon_small is the simplified full geom of this shapefile record, threshold is 1.e-02
        data["is_sequential"] = is_sequential
        # is_sequential is passed as a parameter. If in the temp folder, there are more than one set of records, then
        # is_sequential is True
        data["fire_id"] = fire_id
        # fire_id is passed as a parameter
        data["state"] = state
        # state is passed as a parameter
        logger.info(f"Finished extracting fire record: {path}")
        return data

    @staticmethod
    def _extract_full_geom(shp: shapefile.Reader) -> MultiPolygon:
        """
        Extracts a full geom from a shp reader
        :param shp: shapefile.Reader
        :return: Multipolygon
        """
        return shape(shp.shapeRecord(0).shape.__geo_interface__)

    @staticmethod
    def _simplify_multipolygon(multipolygon: MultiPolygon, threshold: float) -> MultiPolygon:
        """
        Simplifies all components of a multipolygon
        :param multipolygon:shapely.geometry.Multipolygon or shapely.geometry.polygon.Polygon
        :param threshold:float, the threshold of simplification
        :return:shapely.geometry.Multipolygon
        """
        if multipolygon is MultiPolygon:
            # if polygon is a shapely.geometry.MultiPolygon, then it can be convert into a list of
            # shapely.geometry.Polygon
            polygons = list(multipolygon)
        else:
            # if multipolygon is a shapely.geometry.polygon.Polygon, need to explicitly convert into a list
            polygons = [multipolygon]
        # for each polygon in the list of polygons
        # simplify the polygon with object.simplify(tolerance, preserve_topology=True)
        # See https://shapely.readthedocs.io/en/stable/manual.html for more details
        simplified_polygons = [polygon.simplify(threshold) for polygon in polygons]
        # merge polygons into a single multipolygon object and then return it
        return MultiPolygon(simplified_polygons)

    def export(self, file_type: str, file_name: str):
        """
        Useless function for this data pipeline. Keeps it here for abstractmethod
        :param file_type:
        :param file_name:
        :return:
        """
        return


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    fe = FireExtractor()
    print(fe.extract("C:\myResearch\Wildfires\data\\fire-data\ca_trestle_20190605_1200_dd83", True, 0, "ss"))
    # geom1 = fe.extract("C:\myResearch\Wildfires\data\\fire-data\ca_trestle_20190605_1200_dd83", "ca_trestle_20190605_1200_dd83", True, 0, "ss")["geopolygon_full"]
    # geom2 = fe.extract("C:\myResearch\Wildfires\data\\fire-data\ca_trestle_20190605_1200_dd83", "ca_trestle_20190605_1200_dd83", True, 0, "ss")["geopolygon_medium"]
    # assert(geom1 != geom2)

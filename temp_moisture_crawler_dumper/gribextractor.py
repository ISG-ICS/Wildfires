import json
import pygrib
from typing import Dict

from backend.data_preparation.extractor.extractorbase import ExtractorBase


class GRIBExtractor(ExtractorBase):
    TEMPERATURE_MODE = 0
    MOISTURE_MODE = 1

    def __init__(self, filename: str):
        super().__init__(filename)
        self.file_handler = pygrib.open(filename)
        self.data: Dict = dict()

    def extract(self, data_type) -> dict:
        if data_type == GRIBExtractor.TEMPERATURE_MODE:
            # select grib files' attributes
            prop_msg = self.file_handler.select(name='Temperature', typeOfLevel='surface')[0]
        if data_type == GRIBExtractor.MOISTURE_MODE:
            prop_msg = self.file_handler.select(name='Liquid volumetric soil moisture (non-frozen)',
                                                scaledValueOfFirstFixedSurface=0,
                                                scaledValueOfSecondFixedSurface=10)[0]
        prop_dict = dict()  # creates a new dictionary to store data
        prop_vals = prop_msg.values  # values under the started property
        lats, lons = prop_msg.latlons()
        for row_cnt in range(0, len(prop_vals)):
            for col_cnt in range(0, len(prop_vals[row_cnt])):
                prop_dict[str((lats[row_cnt][col_cnt], lons[row_cnt][col_cnt]))] = prop_vals[row_cnt][col_cnt]
        self.data = prop_dict
        return self.data  # the location coordinates are different, don't need to worry about duplicated keys

    def export(self, file_type: str, file_name) -> None:  # json
        if file_type == 'json':
            json.dump(self.data, open(file_name, 'w'))
        # TODO: support other file format like CSV

    def __getitem__(self, lat_lng_pair: tuple) -> float:
        return self.data.get(str(lat_lng_pair))


if __name__ == '__main__':
    # use case of GRIBExtractor, put in the path to the grib file
    grib_extractor = GRIBExtractor('cdas1.t00z.sfluxgrbf00.grib2_20190706.txt')

    # if you want to get temperature data in a dictionary type
    temperature = grib_extractor.extract(data_type=GRIBExtractor.TEMPERATURE_MODE)
    # each item is like: (lat,long):value
    print(temperature)

    # if you want to get moisture data in a dictionary type
    moisture = grib_extractor.extract(data_type=GRIBExtractor.MOISTURE_MODE)
    print(moisture)

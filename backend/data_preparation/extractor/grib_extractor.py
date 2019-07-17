import json
import os
from typing import Dict

import pygrib
import rootpath
from enum import Enum, auto

rootpath.append()
from backend.data_preparation.extractor.extractorbase import ExtractorBase
from paths import TEST_DATA_PATH


class GRIBEnum(Enum):
    NOAA_WIND_U = auto()
    NOAA_WIND_V = auto()
    NOAA_TMP = auto()
    NOAA_SOILW = auto()
    TEMPERATURE_MODE = auto()
    MOISTURE_MODE = auto()


class GRIBExtractor(ExtractorBase):
    NAMES = {
        GRIBEnum.NOAA_WIND_U: {'name': 'U component of wind'},
        GRIBEnum.NOAA_WIND_V: {'name': 'V component of wind'},
        GRIBEnum.NOAA_TMP: {'name': 'Temperature'},
        GRIBEnum.NOAA_SOILW: {'name': 'Volumetric soil moisture content'},
        GRIBEnum.TEMPERATURE_MODE: {'name': 'Temperature', 'typeOfLevel': 'surface'},
        GRIBEnum.MOISTURE_MODE: {'name': 'Volumetric soil moisture content', 'scaledValueOfFirstFixedSurface': 0,
                                 'scaledValueOfSecondFixedSurface': 10},
    }

    def __init__(self, filename: str):
        super().__init__()
        self.file_handler = pygrib.open(filename)
        self.data: Dict

    def extract(self, mode: GRIBEnum) -> dict:
        prop_msg, = self.file_handler.select(**GRIBExtractor.NAMES[mode])
        self.data = dict()  # creates a new dictionary to store data
        prop_values = prop_msg.values  # values under the started property
        lats, longs = prop_msg.latlons()
        for row_cnt in range(0, len(prop_values)):
            for col_cnt in range(0, len(prop_values[row_cnt])):
                self.data[str((lats[row_cnt][col_cnt], longs[row_cnt][col_cnt]))] = prop_values[row_cnt][col_cnt]
        return self.data  # the location coordinates are different, don't need to worry about duplicated keys

    def export(self, file_type: str, file_name) -> None:  # json
        if file_type == 'json':
            json.dump(self.data, open(file_name, 'w'))
        # TODO: support other file format like CSV

    def __getitem__(self, lat_lng_pair: tuple) -> float:
        return self.data.get(str(lat_lng_pair))


if __name__ == '__main__':
    # FIXME: argument mismatching
    grib_extractor = GRIBExtractor(os.path.join(TEST_DATA_PATH, 'cdas1.t00z.sfluxgrbf00.grib2.txt'), 'Temperature',
                                   'surface')
    temperature = grib_extractor[89.84351351786847, 1.8409067652075042]

    print(temperature)

import json
import pygrib

from backend.data_preparation.extractor.extractorbase import ExtractorBase
from typing import Dict

class GRIBExtractor(ExtractorBase):
    def __init__(self, filename: str):
        super().__init__(filename)
        self.file_handler = pygrib.open(filename)
        self.data: Dict = dict()

    def extract(self, prop_name: str, prop_typeOfLevel=None, prop_first=None, prop_second=None) -> dict:
        if prop_typeOfLevel != None:
            prop_msg = self.file_handler.select(name=prop_name, typeOfLevel=prop_typeOfLevel)[0]
        if prop_first != None and prop_second != None:
            prop_msg = self.file_handler.select(name=prop_name, scaledValueOfFirstFixedSurface=prop_first,
                                                scaledValueOfSecondFixedSurface=prop_second)[0]
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
    grib_extractor = GRIBExtractor('../data/recent_temp_mois/cdas1.t00z.sfluxgrbf00.grib2_20190707.txt')
    temperature = grib_extractor.extract(prop_name='Temperature', prop_typeOfLevel='surface')
    moisture = grib_extractor.extract(prop_name='Liquid volumetric soil moisture (non-frozen)', prop_first=0,
                                      prop_second=10)
    print(temperature)
    print(moisture)

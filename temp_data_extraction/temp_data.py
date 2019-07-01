from typing import Dict

import pygrib
import json

class GRIBExtractor:
    def __init__(self, open_file_name, prop_name, prop_typeOfLevel):
        self.file_handler = pygrib.open(open_file_name)
        self.data: Dict = self.extract(prop_name, prop_typeOfLevel)

    def extract(self, prop_name: str, prop_typeOfLevel: str) -> dict:
        prop_msg = self.file_handler.select(name=prop_name, typeOfLevel=prop_typeOfLevel)[0]
        prop_dict = dict()  # creates a new dictionary to store data
        prop_vals = prop_msg.values  # values under the started property
        lats, lons = prop_msg.latlons()
        for row_cnt in range(0, len(prop_vals), 1):
            for col_cnt in range(0, len(prop_vals), 1):
                prop_dict[str((lats[row_cnt][col_cnt], lons[row_cnt][col_cnt]))] = prop_vals[row_cnt][col_cnt]
                print(lats[row_cnt][col_cnt], lons[row_cnt][col_cnt], prop_vals[row_cnt][col_cnt])
        return prop_dict

    def export(self, file_type: str, file_name) -> None:  # json
        if file_type == 'json':
            json.dump(self.data, open(file_name, 'w'))
            return True
        return False

    def __getitem__(self, lat_lng_pair: tuple) -> float:
        for key, value in self.data.items():
            if key == str(lat_lng_pair):
                return value
        return None


if __name__ == '__main__':
    grib_extractor = GRIBExtractor('cdas1.t00z.sfluxgrbf02.grib2.txt', 'Temperature', 'surface')
    temperature = grib_extractor[89.84351351786847, 1.8409067652075042]
    print(temperature)
    print(grib_extractor.export('json','temp_data_with_calss1'))


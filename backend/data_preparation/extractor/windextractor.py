from backend.data_preparation.extractor.extractorbase import ExtractorBase
from configurations import WIND_DATA_DIR, GRIB2_DATA_DIR, GRIB2JSON_PATH
import os
import subprocess
import json


class WindExtractor(ExtractorBase):
    def __init__(self):
        super().__init__('')

    # may use GribConverter or grib2json to convert to json file.
    def extract(self, stamp, useJavaConverter, content=None):

        # create dirs
        if not os.path.isdir(GRIB2_DATA_DIR):
            os.makedirs(GRIB2_DATA_DIR)
        if not os.path.isdir(WIND_DATA_DIR):
            os.makedirs(WIND_DATA_DIR)
        # write file
        with open(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'), 'wb') as f:
            f.write(content)
            print('saved')
        if useJavaConverter:
            # use grib2json
            cmd = [GRIB2JSON_PATH, '--data', '--output',
                   os.path.join(WIND_DATA_DIR, stamp + '.json'), '--names', '--compact',
                   os.path.join(GRIB2_DATA_DIR, stamp + '.f000')]
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                print('converted')
        else:
            # use GribConverter
            try:
                from backend.data_preparation.extractor.GribConverter import GribConverter  # deferred import
                self.data = GribConverter.convert(os.path.join(GRIB2_DATA_DIR, stamp + '.f000'))
                self.export('json', stamp + '.json')
            except ModuleNotFoundError as e:
                print(e)
                print("\n\tpygrib is not supported on Windows, please use '-j' to use grib2json\n")

    def export(self, file_type: str, file_name: str) -> None:
        with open(os.path.join(WIND_DATA_DIR, file_name), 'w') as f:
            json.dump(self.data, f)
        print('converted')

    def __getitem__(self, index):
        return self.data.get(index)

from backend.data_preparation.extractor.extractorbase import ExtractorBase
import os
import subprocess
import json


class WindExtractor(ExtractorBase):
    def __init__(self, filename, prop_name, prop_typeOfLevel):
        super().__init__(filename)

    def extract(self, stamp, useJavaConverter):
        # make dir
        if not os.path.isdir(os.path.join('backend', 'data')):
            os.makedirs(os.path.join('backend', 'data'))
        if useJavaConverter:
            # use grib2json
            cmd = [os.path.join('converter', 'bin', 'grib2json'), '--data', '--output', 'backend/data/latest.json',
                   '--names',
                   '--compact', 'grib-data/' + stamp + '.f000']
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                print('converted')
        else:
            # or use GribConverter
            try:
                from backend.data_preparation.extractor.GribConvertor import GribConvertor  # deferred import
                j = GribConvertor.convert(os.path.join('grib-data', stamp + '.f000'))
                with open(os.path.join('backend', 'data', 'latest.json'), 'w') as f:
                    json.dump(j, f)
                print('converted')
            except ModuleNotFoundError as e:
                print(e)
                print("\n\tpygrib is not supported on Windows, please use '-j' to use grib2json\n")

    def export(self, file_type: str, file_name: str) -> None:
        pass

    def __getitem__(self, index):
        pass

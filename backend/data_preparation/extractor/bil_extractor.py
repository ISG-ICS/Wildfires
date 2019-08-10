import os
import zipfile
from typing import Union, List, Dict

import numpy as np
import rootpath

rootpath.append()

from backend.data_preparation.extractor.extractorbase import ExtractorBase


class BILExtractor(ExtractorBase):
    def __init__(self):
        super().__init__()

    def extract(self, filepath) -> Union[List, Dict]:
        filename = os.path.basename(filepath)
        zf = zipfile.ZipFile(filepath)
        x = os.path.splitext(filepath)[0] + '.hdr'
        y = os.path.pardir()
        zf.extract(os.path.splitext(filepath)[0] + '.hdr', os.path.commonpath(filepath))

    def export(self, file_type: str, file_name: str) -> None:
        pass

    @staticmethod
    def read_prism_hdr(hdr_path):
        """Read an ESRI BIL HDR file"""
        with open(hdr_path, 'r') as input_f:
            header_list = input_f.readlines()
        return dict(item.strip().split() for item in header_list)

    @staticmethod
    def read_prism_bil(bil_path):
        """Read an array from ESRI BIL raster file"""
        hdr_dict = BILExtractor.read_prism_hdr(bil_path.replace('.bil', '.hdr'))
        # For now, only use NROWS, NCOLS, and NODATA
        # Eventually use NBANDS, BYTEORDER, LAYOUT, PIXELTYPE, NBITS

        prism_array = np.fromfile(bil_path, dtype=np.float32)
        prism_array = prism_array.reshape(
            int(hdr_dict['NROWS']), int(hdr_dict['NCOLS']))
        prism_array[prism_array == float(hdr_dict['NODATA'])] = np.nan
        return prism_array

import os
import zipfile

import numpy as np
import rootpath

rootpath.append()

from backend.data_preparation.extractor.extractorbase import ExtractorBase


class BILFormat:
    def __init__(self):
        self.ndarray: np.ndarray = np.zeros(0)
        self.flattened: np.ndarray = np.zeros(0)


class BILExtractor(ExtractorBase):
    # crop:
    # begin point(191, 14)
    # (228, 248)
    crop_top = 191
    crop_bottom = 419
    crop_left = 14
    crop_right = 262

    def extract(self, filepath) -> BILFormat:
        # extract files
        filename = os.path.basename(filepath)
        zf = zipfile.ZipFile(filepath)

        zf.extract(os.path.splitext(filename)[0] + '.hdr', os.path.split(filepath)[0])
        zf.extract(os.path.splitext(filename)[0] + '.bil', os.path.split(filepath)[0])
        header_path = os.path.join(os.path.split(filepath)[0], os.path.splitext(filename)[0] + '.hdr')
        bil_path = os.path.join(os.path.split(filepath)[0], os.path.splitext(filename)[0] + '.bil')

        # read header and BIL
        bil: BILFormat = BILExtractor.read_prism_bil(header_path, bil_path)

        # clean up
        os.remove(header_path)
        os.remove(bil_path)

        return bil

    def export(self, file_type: str, file_name: str) -> None:
        pass

    @staticmethod
    def read_prism_bil(hdr_path, bil_path) -> BILFormat:
        """Read an array from ESRI BIL raster file"""
        hdr_dict = BILExtractor.read_prism_hdr(hdr_path)
        # For now, only use NROWS, NCOLS, and NODATA
        # Eventually use NBANDS, BYTEORDER, LAYOUT, PIXELTYPE, NBITS

        prism_array = np.fromfile(bil_path, dtype=np.float32)  # type: np.ndarray
        prism_array = prism_array.reshape(
            int(hdr_dict['NROWS']), int(hdr_dict['NCOLS']))

        # replace -9999 with np.nan
        # prism_array[prism_array == float(hdr_dict['NODATA'])] = np.nan

        bil = BILFormat()

        bil.ndarray = prism_array[BILExtractor.crop_top:BILExtractor.crop_bottom,
                      BILExtractor.crop_left:BILExtractor.crop_right]
        bil.flattened = prism_array.flatten()
        return bil

    @staticmethod
    def read_prism_hdr(hdr_path):
        """Read an ESRI BIL HDR file"""
        with open(hdr_path, 'r') as input_f:
            header_list = input_f.readlines()
        # noinspection PyTypeChecker
        return dict(item.strip().split() for item in header_list)


if __name__ == '__main__':
    ext = BILExtractor()
    print(ext.extract('E:\\Projects\\Wildfires\\data\\PRISM\\PRISM_ppt_early_4kmD2_20190802_bil.zip'))

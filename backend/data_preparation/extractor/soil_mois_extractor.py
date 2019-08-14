import json
import os

import fiona
import numpy as np
import rasterio
import rasterio.mask
import rootpath
from osgeo import gdal

rootpath.append()
from paths import US_SHAPE_PATH
from backend.data_preparation.extractor.extractorbase import ExtractorBase
from paths import SOIL_MOIS_DATA_DIR


class SoilMoisExtractor(ExtractorBase):
    def __init__(self):
        super().__init__()
        self.data: list = []

    def extract(self, file_path):
        with fiona.open(US_SHAPE_PATH, "r") as shapefile:
            features = [feature["geometry"] for feature in shapefile]

        temp_new_res_image = os.path.join(SOIL_MOIS_DATA_DIR, 'new_res.tif')
        temp_masked_image = os.path.join(SOIL_MOIS_DATA_DIR, 'masked_image.tif')
        # change resolution of the image, put it into a temporary 'new_res.tif', will be deleted automatically
        os.system(
            f'gdalwarp -r bilinear -tr 0.041666667 0.041666667 -t_srs "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs" -overwrite {file_path} {temp_new_res_image}')

        # use the us shape to mask the 'new_res.tif'
        with rasterio.open(temp_new_res_image) as src:
            out_image, out_transform = rasterio.mask.mask(src, features, crop=True)
            out_meta = src.meta.copy()

        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        # save the masked image as 'masked_image.tif'
        with rasterio.open(temp_masked_image, "w", **out_meta) as dest:
            dest.write(out_image)

        # get the list from the tif image
        file = gdal.Open(temp_masked_image)
        self.data = file.ReadAsArray().tolist()

        # remove the temporary images and the original data file
        os.remove(temp_new_res_image)
        os.remove(temp_masked_image)
        os.remove(file_path)

        return self.data  # the location coordinates are different, don't need to worry about duplicated keys

    def export(self, file_type: str, file_name) -> None:  # json
        if file_type == 'json':
            json.dump(self.data, open(file_name, 'w'))
        # TODO: support other file format like CSV


if __name__ == '__main__':
    soil_mois_extractor = SoilMoisExtractor()
    data = soil_mois_extractor.extract(os.path.join(SOIL_MOIS_DATA_DIR, '20190812.tif'))
    print(np.array(data).shape)

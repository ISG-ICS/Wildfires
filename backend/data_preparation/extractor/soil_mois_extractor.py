import json
import logging
import os
from datetime import datetime

import fiona
import gdal
import numpy as np
import rasterio
import rasterio.mask
import rootpath

rootpath.append()
from backend.data_preparation.crawler.soil_mois_crawler import SoilMoisCrawler
from paths import US_SHAPE_PATH
from backend.data_preparation.extractor.extractorbase import ExtractorBase
from paths import SOIL_MOIS_DATA_DIR

logger = logging.getLogger('TaskManager')


class TiffExtractor(ExtractorBase):
    def __init__(self):
        super().__init__()
        self.data = []

    def extract(self, file_path: str) -> np.ndarray:
        temp_new_res_image_path = os.path.join(SOIL_MOIS_DATA_DIR, 'new_res.tif')
        temp_masked_image_path = os.path.join(SOIL_MOIS_DATA_DIR, 'masked_image.tif')
        # change resolution of the image, put it into a temporary 'new_res.tif', will be deleted automatically
        os.system(
            f'gdalwarp -r bilinear -tr 0.041666667 0.041666667 -t_srs '
            f'"+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs" -overwrite {file_path} {temp_new_res_image_path}')
        logger.info(f"file: {file_path} changed resolution, {temp_new_res_image_path} created")

        # use the us bounding box to mask the 'new_res.tif'
        US_west = -125 - 1 / 48  # x_min
        US_south = 24.083333333335364 - 1 / 48  # y_min
        US_east = -66.5 + 1 / 48  # x_max
        US_north = 49.9166666666687 + 1 / 48  # y_max
        os.system(
            f'gdalwarp -te {US_west} {US_south} {US_east} {US_north} {temp_new_res_image_path} {temp_masked_image_path}')
        logger.info(f"file: {file_path} image cut to US, {temp_masked_image_path} created")
        self.data = np.array(gdal.Open(temp_masked_image_path).ReadAsArray())
        logger.info(f"file: {file_path} data extracted from {temp_masked_image_path}")

        # remove the temporary image files
        os.remove(temp_new_res_image_path)
        logger.info(f"file: {temp_new_res_image_path} removed")
        os.remove(temp_masked_image_path)
        logger.info(f"file: {temp_masked_image_path} removed")

        return self.data

    def export(self, file_type: str, file_name) -> None:  # json
        if file_type == 'json':
            json.dump(self.data, open(file_name, 'w'))
        # TODO: support other file format like CSV

    @staticmethod
    def mask_by_us_shape(src_path, dest_path):
        # this can be removed if the function is not going to be used
        with fiona.open(US_SHAPE_PATH, "r") as shapefile:
            features = [feature["geometry"] for feature in shapefile]
        with rasterio.open(src_path) as src:
            out_image, out_transform = rasterio.mask.mask(src, features, crop=True)
            out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})

        # save the masked image
        with rasterio.open(dest_path, "w", **out_meta) as dest:
            dest.write(out_image)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    crawler = SoilMoisCrawler()
    soil_mois_extractor = TiffExtractor()
    target_date = "20131230"

    file_path = crawler.crawl(datetime.strptime(target_date, SoilMoisCrawler.TIME_FORMAT))
    if file_path is not None:
        data = soil_mois_extractor.extract(file_path)
        print(np.array(data).shape)

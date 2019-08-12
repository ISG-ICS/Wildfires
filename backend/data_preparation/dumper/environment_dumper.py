import os
import logging
import traceback
import rootpath
import paths
from PIL import Image
import numpy as np

rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.classifiers.environment_classifier import EnvironmentClassifier
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')


class EnvironmentDumper(DumperBase):
    INSERT_CONSTANT_FEATURES = 'INSERT INTO "constant_env_features" (gid, landcover, elevation, aspect, slope) ' \
                               'VALUES (%s, %s, %s, %s, %s)'
    INSERT_SOIL_MOISTURE = 'INSERT INTO "soil_moisture" (gid, datetime, soil_moisture) ' \
                           'VALUES (%s, %s, %s)'
    INSERT_NDVI = 'INSERT INTO "ndvi" (gid, datetime, ndvi) ' \
                  'VALUES (%s, %s, %s)'
    INSERT_ENV_PREDICTION = 'INSERT INTO env_features_prediction(gid, datetime, wildfire_probability) ' \
                            'values (%s, %s, %s)'
    SELECT_ENV_DATETIME = 'select datetime from env_features_prediction'
    UPDATE_ENV_PREDICTION = 'UPDATE env_features_prediction SET wildfire_probability = %s WHERE gid = %s and datetime = %s'

    def insert(self, prediction_result, datetime):
        print(datetime)
        insert_flag = 1
        try:
            temp_set = Connection().sql_execute(EnvironmentDumper.SELECT_ENV_DATETIME)
            datetime_set = set()
            for i in temp_set:
                datetime_set.add(str(i[0]) + str('.000000'))
            print(datetime_set)
            if datetime in datetime_set:
                insert_flag = 0
        except Exception:
            logger.error("error: " + traceback.format_exc())

        gid = 0
        for i in range(len(prediction_result)):
            for j in range(len(prediction_result[i])):
                try:
                    with Connection() as conn:
                        cur = conn.cursor()
                        if insert_flag:
                            cur.execute(EnvironmentDumper.INSERT_ENV_PREDICTION,
                                        (gid, datetime, prediction_result[gid // EnvironmentClassifier.ENV_IMG_COLUMN][
                                            gid % EnvironmentClassifier.ENV_IMG_COLUMN]))
                        else:
                            cur.execute(EnvironmentDumper.UPDATE_ENV_PREDICTION,
                                        (prediction_result[gid // EnvironmentClassifier.ENV_IMG_COLUMN][
                                             gid % EnvironmentClassifier.ENV_IMG_COLUMN], gid, datetime))
                        gid += 1
                        conn.commit()
                        cur.close()
                except Exception:
                    logger.error("error: " + traceback.format_exc())

    def insert_constant_feature(self, landcover: list, elevation: list, aspect: list, slope: list):
        """insert four constant environmental features into database"""
        gid = 0

        with Connection() as conn:
            cur = conn.cursor()

            for i in range(len(landcover)):
                for j in range(len(landcover[i])):
                    labdcover_value = landcover[i][j]
                    elevation_value = elevation[i][j]
                    aspect_value = aspect[i][j]
                    slope_value = slope[i][j]

                    try:
                        cur.execute(EnvironmentDumper.INSERT_CONSTANT_FEATURES,
                                    (gid, labdcover_value, elevation_value, aspect_value, slope_value))
                        gid += 1
                    except Exception:
                        logger.error("error: " + traceback.format_exc())

            conn.commit()
            cur.close()

    def insert_weekly_feature(self, datetime: str, weekly_feature: list, feature_type: str):
        gid = 0
        if feature_type == "soil_moisture":
            insert_statement = EnvironmentDumper.INSERT_SOIL_MOISTURE
        elif feature_type == "ndvi":
            insert_statement = EnvironmentDumper.INSERT_NDVI

        with Connection() as conn:
            cur = conn.cursor()

            for i in range(len(weekly_feature)):
                for j in range(len(weekly_feature[i])):
                    weekly_feature_value = weekly_feature[i][j]
                    try:
                        cur.execute(insert_statement,
                                    (gid, datetime, weekly_feature_value))
                    except Exception:
                        logger.error("error: " + traceback.format_exc())
                    gid += 1
                print(gid)
            conn.commit()
            cur.close()

    def tif_to_list(self, tif_path):
        im = Image.open(tif_path)
        imarray = np.array(im).tolist()
        return imarray


if __name__ == '__main__':
    # Case 1:
    landcover_path = os.path.join(paths.ROOT_DIR, 'data/constant_env_features/landcover_CA.tif')
    landcover = EnvironmentDumper().tif_to_list(landcover_path)

    elevation_path = os.path.join(paths.ROOT_DIR, 'data/constant_env_features/elevation_CA.tif')
    elevation = EnvironmentDumper().tif_to_list(elevation_path)

    aspect_path = os.path.join(paths.ROOT_DIR, 'data/constant_env_features/aspect_CA.tif')
    aspect = EnvironmentDumper().tif_to_list(aspect_path)

    slope_path = os.path.join(paths.ROOT_DIR, 'data/constant_env_features/slope_CA.tif')
    slope = EnvironmentDumper().tif_to_list(slope_path)

    EnvironmentDumper().insert_constant_feature(landcover, elevation, aspect, slope)

    # Case 2:
    soil_moisture_path = os.path.join(paths.ROOT_DIR, 'data/4soil_moisture/sm201809171.tif')
    soil_moisture = EnvironmentDumper().tif_to_list(soil_moisture_path)
    datetime = '2018-09-17 00:00:00.000000'

    EnvironmentDumper().insert_weekly_feature(datetime, soil_moisture, "soil_moisture")

    # Case 3:
    ndvi_path = os.path.join(paths.ROOT_DIR, 'data/5NDVI/NDVI201809111.tif')
    ndvi = EnvironmentDumper().tif_to_list(ndvi_path)
    datetime = '2018-09-11 00:00:00.000000'

    EnvironmentDumper().insert_weekly_feature(datetime, ndvi, "ndvi")

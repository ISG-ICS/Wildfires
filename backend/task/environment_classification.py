import logging
import traceback

from typing import Union, List, Dict


import torch
import numpy as np
import codecs
import rootpath

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.connection import Connection
from backend.classifiers.environment_classifier import EnvironmentClassifier
from backend.data_preparation.dumper.environment_dumper import EnvironmentDumper

logger = logging.getLogger('TaskManager')


class EnvironmentClassification(Runnable):

    def run(self, datetime: str = None, ndvi_weektime: str = None, soil_weektime: str = None):
        environment_classifier = EnvironmentClassifier()

        environment_dumper = EnvironmentDumper()

        environment_classifier.set_model()

        env_features = self.make_input_dataset(datetime, ndvi_weektime, soil_weektime)

        prediction_result = environment_classifier.predict(env_features)

        environment_dumper.insert(prediction_result, datetime)

    def make_input_dataset(self, datetime: str = None, ndvi_weektime: str = None, soil_weektime: str = None):
        ####### TODO:
        # ppt, tmax, vpdmax
        us_ppt = self.asc_to_numpy('PRISM_ppt_stable_4kmD2_20180911_asc.asc')
        us_tmax = self.asc_to_numpy('PRISM_tmax_stable_4kmD1_20180911_asc.asc')
        us_vpdmax = self.asc_to_numpy('PRISM_vpdmax_stable_4kmD1_20180911_asc.asc')

        ca_ppt = self.extract_region(us_ppt)
        ca_tmax = self.extract_region(us_tmax)
        ca_vpdmax = self.extract_region(us_vpdmax)

        ca_ppt = torch.unsqueeze(torch.tensor(ca_ppt), dim=0)
        ca_tmax = torch.unsqueeze(torch.tensor(ca_tmax), dim=0)
        ca_vpdmax = torch.unsqueeze(torch.tensor(ca_vpdmax), dim=0)
        #######

        # landcover, elevation, aspect, slope, ndvi, soil_moisture
        ca_landcover = np.zeros((1, 228, 248))
        ca_elevation = np.zeros((1, 228, 248))
        ca_aspect = np.zeros((1, 228, 248))
        ca_slope = np.zeros((1, 228, 248))
        ca_ndvi = np.zeros((1, 228, 248))
        ca_soil_moisture = np.zeros((1, 228, 248))

        try:
            for gid, landcover, elevation, aspect, slope in Connection().sql_execute \
                        ("select gid, landcover, elevation, aspect, slope from env_constant_features"):
                ca_landcover[0][int(gid // 248)][int(gid % 248)] = landcover
                ca_elevation[0][int(gid // 248)][int(gid % 248)] = elevation
                ca_aspect[0][int(gid // 248)][int(gid % 248)] = aspect
                ca_slope[0][int(gid // 248)][int(gid % 248)] = slope

            if datetime:
                for gid, ndvi in Connection().sql_execute \
                            ("select gid, ndvi from env_ndvi where datetime = '{}'".format(ndvi_weektime)):
                    ca_ndvi[0][int(gid // 248)][int(gid % 248)] = ndvi

                for gid, sm in Connection().sql_execute \
                            ("select gid, soil_moisture from env_soil_moisture where datetime = '{}'".format(soil_weektime)):
                    ca_soil_moisture[0][int(gid // 248)][int(gid % 248)] = sm
            else:
                # datetime is None, fetch all
                # TODO
                pass
        except:
            logger.error('error: ' + traceback.format_exc())

        total_input = np.concatenate((ca_ppt, ca_tmax), axis=0)
        total_input = np.concatenate((total_input, ca_vpdmax), axis=0)
        total_input = np.concatenate((total_input, ca_landcover), axis=0)
        total_input = np.concatenate((total_input, ca_elevation), axis=0)
        total_input = np.concatenate((total_input, ca_aspect), axis=0)
        total_input = np.concatenate((total_input, ca_slope), axis=0)
        total_input = np.concatenate((total_input, ca_ndvi), axis=0)
        # total_input = np.concatenate((total_input, ca_soil_moisture), axis=0)

        return total_input

    def asc_to_numpy(self, imgpath):
        X = []
        count = 0
        with codecs.open(imgpath, encoding='utf-8-sig') as f:
            for line in f:
                count += 1
                if count <= 6:
                    continue
                s = line.split()
                X.append([float(s[i]) for i in range(len(s))])

        X = np.array(X)
        return X

    def extract_region(self, X, top_idx: int = 191, bottom_idx: int = 418, left_idx: int = 13, right_idx: int = 260):
        region = []
        for lat in range(top_idx, bottom_idx + 1):
            row = X[lat][left_idx:right_idx + 1]
            region.append(row)
        return np.array(region)

    def normalize(self, numpy_arr):
        normalized_train_set = []
        for i in range(len(numpy_arr)):
            amin, amax = numpy_arr[i].min(), numpy_arr[i].max()
            arr = (numpy_arr[i] - amin) / (amax - amin)
            normalized_train_set.append(arr * 100)
        return np.array(normalized_train_set)

    # def make(self):
    #     # ppt, tmax, vpdmax
    #     us_ppt = self.asc_to_numpy('PRISM_ppt_stable_4kmD2_20180911_asc.asc')
    #     us_tmax = self.asc_to_numpy('PRISM_tmax_stable_4kmD1_20180911_asc.asc')
    #     us_vpdmax = self.asc_to_numpy('PRISM_vpdmax_stable_4kmD1_20180911_asc.asc')
    #
    #     ca_ppt = self.extract_region(us_ppt)
    #     ca_tmax = self.extract_region(us_tmax)
    #     ca_vpdmax = self.extract_region(us_vpdmax)
    #
    #     ca_ppt = torch.unsqueeze(torch.tensor(ca_ppt), dim=0)
    #     ca_tmax = torch.unsqueeze(torch.tensor(ca_tmax), dim=0)
    #     ca_vpdmax = torch.unsqueeze(torch.tensor(ca_vpdmax), dim=0)
    #
    #     total_input = np.concatenate((ca_ppt, ca_tmax), axis=0)
    #     total_input = np.concatenate((total_input, ca_vpdmax), axis=0)
    #
    #     # landcover, elevation, aspect, slope
    #     ca_landcover = np.zeros((1, 228, 248))
    #     ca_elevation = np.zeros((1, 228, 248))
    #     ca_aspect = np.zeros((1, 228, 248))
    #     ca_slope = np.zeros((1, 228, 248))
    #
    #     try:
    #         print("try...")
    #         for gid, landcover, elevation, aspect, slope in Connection().sql_execute \
    #                     ("select gid, landcover, elevation, aspect, slope from constant_env_features"):
    #             ca_landcover[0][int(gid // 248)][int(gid % 248)] = landcover
    #             ca_elevation[0][int(gid // 248)][int(gid % 248)] = elevation
    #             ca_aspect[0][int(gid // 248)][int(gid % 248)] = aspect
    #             ca_slope[0][int(gid // 248)][int(gid % 248)] = slope
    #
    #     except:
    #         logger.error('error: ' + traceback.format_exc())
    #     print("done!")
    #
    #     total_input = np.concatenate((total_input, ca_landcover), axis=0)
    #     total_input = np.concatenate((total_input, ca_elevation), axis=0)
    #     total_input = np.concatenate((total_input, ca_aspect), axis=0)
    #     total_input = np.concatenate((total_input, ca_slope), axis=0)
    #
    #     # ndvi, soil_moisture
    #     ca_ndvi = np.zeros((1, 228, 248))
    #     ca_soil_moisture = np.zeros((1, 228, 248))
    #     try:
    #         print("try...")
    #         for gid, ndvi in Connection().sql_execute \
    #                     ("select gid, ndvi from ndvi where datetime = '2018-09-11 00:00:00.000000'"):
    #             ca_ndvi[0][int(gid // 248)][int(gid % 248)] = ndvi
    #
    #         for gid, sm in Connection().sql_execute \
    #                     ("select gid, soil_moisture from soil_moisture where datetime = '2018-09-10 00:00:00.000000'"):
    #             ca_soil_moisture[0][int(gid // 248)][int(gid % 248)] = sm
    #
    #     except:
    #         logger.error('error: ' + traceback.format_exc())
    #     print("done!")
    #     total_input = np.concatenate((total_input, ca_ndvi), axis=0)
    #     # total_input = np.concatenate((total_input, ca_soil_moisture), axis=0)
    #
    #     return total_input


if __name__ == '__main__':
    # EnvironmentClassification().run()
    EnvironmentClassification().run(datetime='2018-09-11 00:00:00.000000',
                                    ndvi_weektime='2018-09-11 00:00:00.000000',
                                    soil_weektime='2018-09-10 00:00:00.000000')

from typing import Tuple

import numpy as np
import pandas as pd
import sys
import os
import glob
import linecache

from backend.data_preparation.extractor.extractorbase import ExtractorBase



class PRISMExtractor(ExtractorBase):
    def export(self, file_type: str, file_name: str) -> None:
        pass

    def __init__(self):
        pass

    @staticmethod
    def _f():
        pass

    def extract(self, input_file: str, input_time: str, input_param: str) -> Tuple[float, float, float, float, np.ndarray]:
        """extracts the data from asc file and return as a tuple"""
        ncols = float(linecache.getline(input_file, 1).strip().split()[1])
        nrows =  float(linecache.getline(input_file, 2).strip().split()[1])
        xllcorner = float(linecache.getline(input_file, 3).strip().split()[1])
        yllcorner = float(linecache.getline(input_file, 4).strip().split()[1])
        cellsize = float(linecache.getline(input_file, 5).strip().split()[1])
        null_data = float(linecache.getline(input_file, 6).strip().split()[1])

        ascii_grid = np.loadtxt(input_file, skiprows=6)
        return ncols, nrows, xllcorner, yllcorner, cellsize, null_data, ascii_grid



if __name__ == "__main__":
    input_file = glob.glob("/home/uechi/local_github/schun/test_data_set/*.asc")
    input_file = sorted(input_file)

    ex_file = PRISMExtractor()

    input_file_name = []
    for i in range(0, len(input_file)):
        input_file_name.append(input_file[i].split("/")[-1])

    l_head = []
    l_param = []
    l_early = []
    l_dim = []
    l_time = []
    l_ext = []
    for i in range(0, len(input_file_name)):
        head, param, early, dim, time, ext = input_file_name[i].split("_")

        l_head.append(head)
        l_param.append(param)
        l_early.append(early)
        l_dim.append(dim)
        l_time.append(time)
        l_ext.append(ext)

    u_l_head = list(set(l_head))
    u_l_param = list(set(l_param))
    u_l_early = list(set(l_early))
    u_l_dim = list(set(l_dim))
    u_l_time = list(set(l_time))
    u_l_ext = list(set(l_ext))

    u_l_head.sort()
    u_l_param.sort()
    u_l_early.sort()
    u_l_dim.sort()
    u_l_time.sort()
    u_l_ext.sort()

    time_dict = dict()
    for i1 in range(0, len(u_l_time)):

        param_dict = dict()
        for i2 in range(0, len(u_l_param)):
            if u_l_param[i2] == "ppt":
                ext_filename = str(u_l_head[0] + "_" + u_l_param[i2] + "_" + u_l_early[0] + "_" + "4kmD2" + "_" + u_l_time[i1] + "_" + u_l_ext[0])
            else:
                ext_filename = str(u_l_head[0] + "_" + u_l_param[i2] + "_" + u_l_early[0] + "_" + "4kmD1" + "_" + u_l_time[i1] + "_" + u_l_ext[0])

            ncols, nrows, xllcorner, yllcorner, cellsize, null_data, ascii_grid = ex_file.extract(input_file[i], param, time)

            values_dict = dict()
            for j1 in range(0, int(nrows)):
                for j2 in range(0, int(ncols)):
                    #print(j1, j2, ascii_grid[j1][j2], "gps_nconls=", xllcorner + cellsize * (ncols - j1), "gps_nconls=", yllcorner + cellsize * (nrows - j2))

                    lat = xllcorner + cellsize * (ncols - j1)
                    long = yllcorner + cellsize * (nrows - j2)
                    value = ascii_grid[j1][j2]

                    lat_long = (lat, long)
                    values_dict[lat_long] = value

            param_dict[u_l_param[i2]] = values_dict
        time_dict[u_l_time[i1]] = param_dict
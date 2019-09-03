# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 14:10:00 2019

@author: LiShu
"""

import numpy as np
import pandas as pd


def change_resolution(row, col, resolution_custom):
    # new latitude and longitude
    n_row_custom = int(row // (resolution_custom // resolution_default)) + 1
    n_col_custom = int(col // (resolution_custom // resolution_default)) + 1
    lat = []
    lon = []
    for row in range(n_row_custom):
        lat.append(yllcorner + resolution_custom * (n_row_custom - row))
    for column in range(n_col_custom):
        lon.append(xllcorner + resolution_custom * column)

    data_change_resolution = []
    cell = []

    for row in range(n_row_custom - 1):
        for column in range(n_col_custom - 1):
            n = 0
            rainfall = 0
            for i in data_resolution_default:
                if lat[row] > i[0] > lat[row + 1] and lon[column] < i[1] < lon[column + 1] and i[2] >= 0:
                    n += 1
                    rainfall = rainfall + i[2]
                elif i[0] < lat[row + 1] and i[1] > lon[column + 1]:
                    break
            cell.append((lat[row] + lat[row + 1]) / 2)
            cell.append((lon[column] + lon[column + 1]) / 2)
            if n == 0:
                cell.append(-99.0)
            else:
                cell.append(rainfall / n)
            data_change_resolution.append(cell)
            cell = []
    return data_change_resolution


# import starting point corrdinates and resolution from .asc file
asc_file = pd.read_csv(r"data/CCS_1h2019062400.asc")
xllcorner = float(asc_file.iat[1, 0][10:18])
yllcorner = float(asc_file.iat[2, 0][10:18])
resolution_default = float(asc_file.iat[3, 0][9:13])

# convert .asc to array
ascii_grid = np.loadtxt(r"data/CCS_1h2019062400.asc", skiprows=6)
n_row = ascii_grid.shape[0]
n_col = ascii_grid.shape[1]

# generate list [lat,lon,rainfall]
cell = []
data_resolution_default = []
for r in range(n_row):
    for c in range(n_col):
        cell.append(yllcorner + resolution_default * (n_row - r))
        cell.append(xllcorner + resolution_default * c)
        cell.append(ascii_grid[r, c])
        data_resolution_default.append(cell)
        cell = []

# generate .csv
test = pd.DataFrame(data=data_resolution_default)
test.to_csv('data/testcsv.csv', encoding='gbk')

# change resolution
Data_resolution_custom = change_resolution(n_row, n_col, 0.4)
test = pd.DataFrame(data=Data_resolution_custom)
test.to_csv('data/testcsv.csv', encoding='gbk')

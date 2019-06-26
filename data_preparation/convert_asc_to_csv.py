# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 14:10:00 2019

@author: LiShu
"""

import numpy as np
import pandas as pd

def change_resolution(row, col, resolution_custom):
    # new latitidue and longitude
    nrow_custom = int(row // (resolution_custom//resolution_default))+1
    ncol_custom = int(col // (resolution_custom//resolution_default))+1
    lat = []
    lon = []
    for r in range(nrow_custom):
        lat.append(yllcorner + resolution_custom*(nrow_custom-r))
    for c in range(ncol_custom):
        lon.append(xllcorner + resolution_custom*c)
    
    Data_change_resolution = []
    cell = []
    
    for r in range(nrow_custom-1):
        for c in range(ncol_custom-1):
            n = 0
            rainfall = 0
            for i in Data_resolution_default:
                if i[0]<lat[r] and i[0]>lat[r+1] and i[1]>lon[c] and i[1]<lon[c+1] and i[2] >=0:
                    n += 1
                    rainfall = rainfall + i[2]
                elif i[0]<lat[r+1] and i[1] > lon[c+1]:
                    break
            cell.append((lat[r]+lat[r+1])/2)
            cell.append((lon[c]+lon[c+1])/2)
            if n == 0:
                cell.append(-99.0)
            else:
                cell.append(rainfall/n)
            Data_change_resolution.append(cell)
            cell = []
    return(Data_change_resolution)
    
    
#import starting point corrdinates and resolution from .asc file
ascfile=pd.read_csv(r"D:\CCS_1h2019062400.asc")
xllcorner = float(ascfile.iat[1,0][10:18])
yllcorner = float(ascfile.iat[2,0][10:18])
resolution_default = float(ascfile.iat[3,0][9:13])

# convert .asc to array
ascii_grid = np.loadtxt(r"D:\CCS_1h2019062400.asc", skiprows=6)
nrow = ascii_grid.shape[0]
ncol = ascii_grid.shape[1]

# generate list [lat,lon,rainfall]
cell = []
Data_resolution_default = []
for r in range(nrow):
    for c in range(ncol):
        cell.append(yllcorner + resolution_default*(nrow-r))
        cell.append(xllcorner + resolution_default*c)
        cell.append(ascii_grid[r,c])
        Data_resolution_default.append(cell)
        cell = []

# generate .csv
test=pd.DataFrame(data=Data_resolution_default)
test.to_csv('d:/testcsv.csv',encoding='gbk')

#change resolution
Data_resolution_custom = change_resolution(nrow, ncol, 0.4)
test=pd.DataFrame(data=Data_resolution_custom)
test.to_csv('d:/testcsv.csv',encoding='gbk')




        
        



"""
Script to convert from ASCII Raster Format to XYZ format (Mohid Model)
@wrenteria
30/11/2017
"""

import numpy as np


class ASC2XYZ():
    def __init__(self, inputfile):
        self.inputfile = inputfile

    def extract(self):
        # If bathymetry data is positive change  Line 23
        # If longitude data is -180 +180, change Line 27

        dictionary = dict()
        time = self.inputfile.split('_')[-2]
        idict = {}
        par = open(self.inputfile)
        dat = np.loadtxt(self.inputfile, skiprows=6)
        # dat=dat*-1
        nc = int(par.readline().split()[1])
        nr = int(par.readline().split()[1])
        xl = float(par.readline().split()[1])
        yl = float(par.readline().split()[1])
        cs = float(par.readline().split()[1])
        ndv = int(par.readline().split()[1])
        lons = []
        lats = []
        temp_dict = dict()
        for i in range(nc):
            lons.append(xl)
            xl = xl + cs

        for i in range(nr):
            lats.append(yl)
            yl = yl + cs
        for j in range(nr):
            for i in range(nc):
                if dat[j, i] != ndv and lons[i] > -118 and lons[i] < -114 and lats[-j] > 32 and lats[-j] < 34:
                    temp_dict[lats[-j], lons[i]] = dat[j, i]
                    idict.update(temp_dict)
        dictionary[time] = idict
        return dictionary


if __name__ == '__main__':
    input = '/Users/gutingxuan/Desktop/Wildfires/satellite_classification/PRISM_ppt_stable_4kmD2_20180901_asc.asc'
    extractor = ASC2XYZ(input)
    dict_ = extractor.extract()
    print(dict_)

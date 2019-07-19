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
        # outputfile = self.inputfile + 'output.xyz'
        # If bathymetry data is positive change  Line 19
        # If longitude data is -180 +180, change Line 22

        dictionary = dict()
        time = self.inputfile.split('_')[-2]
        idict = {}
        par = open(self.inputfile)
        dat = np.loadtxt(self.inputfile, skiprows=6)
        # out = open(outputfile, 'w')
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
        #             out.write('{:3.4f} {:3.4f} {:3.4f}'.format(lons[i], lats[-j], dat[j, i]) + '\n')
        # out.close()

        # time = self.inputfile.split('_')[-2]
        # dictionary = dict()
        # xyzFile = open(self.inputfile + 'output.xyz')
        # line = xyzFile.readline()
        # idict = {}
        # while line:  # get dictionary from the xyzfile
        #     lat, long_, value = self.get_lat_long_value(line)
        #     temp_dict = dict()
        #     lat = float(lat)
        #     long_ = float(long_)
        #     value = float(value)
        #     temp_dict[lat, long_] = value
        #     # if lat > 32 and lat < 42 and long_ > -124 and long_ < -114:
        #     if lat > 32 and lat < 34 and long_ > -118 and long_ < -114:
        #         idict.update(temp_dict)
        #     line = xyzFile.readline()
        # dictionary[time]=idict
        # return dictionary

    def get_lat_long_value(self, line):
        long_, lat, value = line.split(' ')
        value = value.strip('\n')
        return lat, long_, value


if __name__ == '__main__':
    input = '/Users/gutingxuan/Desktop/Wildfires/satellite_classification/PRISM_ppt_stable_4kmD2_20180801_asc.asc'
    out = open('/Users/gutingxuan/Desktop/Wildfires/satellite_classification/output1.txt', 'w')
    par = open(input)
    dat = np.loadtxt(input, skiprows=6)
    # dat=dat*-1
    nc = int(par.readline().split()[1])
    nr = int(par.readline().split()[1])
    xl = float(par.readline().split()[1])
    yl = float(par.readline().split()[1])
    cs = float(par.readline().split()[1])
    ndv = int(par.readline().split()[1])
    lons = []
    lats = []
    for i in range(nc):
        lons.append(xl)
        xl = xl + cs

    for i in range(nr):
        lats.append(yl)
        yl = yl + cs
    for j in range(nr):
        for i in range(nc):
            if dat[j, i] != ndv and lons[i] > -118 and lons[i] < -114 and lats[-j] > 32 and lats[-j] < 34:
                out.write('{:3.4f} {:3.4f} {:3.4f}'.format(lons[i], lats[-j], dat[j, i]) + '\n')
    out.close()

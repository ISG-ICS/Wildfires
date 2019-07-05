import requests
from datetime import datetime, timedelta
import math
import os
import subprocess
import sys
import json

baseDir = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl'
useJavaConverter = False  # use grib2json?


def main():
    for arg in sys.argv:
        if arg == '-j':
            global useJavaConverter
            useJavaConverter = True
    t = datetime.today()
    runQuery(t + timedelta(hours=6))


def runQuery(t):
    time = t.timetuple()
    date = t.strftime('%Y%m%d')
    hour = roundHour(time.tm_hour, 6)
    stamp = date + hour
    stamp2 = date + '/' + hour

    # parameters of GET
    qs = {
        'file': 'gfs.t' + hour + 'z.pgrb2.0p25.anl',
        'lev_20_m_above_ground': 'on',
        'var_UGRD': 'on',
        'var_VGRD': 'on',
        'leftlon': 0,
        'rightlon': 360,
        'toplat': 90,
        'bottomlat': -90,
        'dir': '/gfs.' + stamp2
    }
    try:
        r = requests.get(url=baseDir, params=qs)
        if r.status_code != 200:
            # try -6h
            print(stamp + ' not found')
            runQuery(t - timedelta(hours=6))
        else:
            # create dirs
            if not os.path.isdir('grib-data'):
                os.makedirs('grib-data')
            # write file
            with open(os.path.join('grib-data', stamp + '.f000'), 'wb') as f:
                f.write(r.content)
            print('saved')

            # convert format
            convert(stamp)
    except IOError as e:
        # try -6h
        print(e)
        runQuery(t - timedelta(hours=6))


def convert(stamp):
    if not os.path.isdir(os.path.join('backend', 'data')):
        os.makedirs(os.path.join('backend', 'data'))
    if useJavaConverter:
        cmd = [os.path.join('converter', 'bin', 'grib2json'), '--data', '--output', 'backend/data/latest.json',
               '--names',
               '--compact', 'grib-data/' + stamp + '.f000']
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        process.wait()
        if process.returncode == 0:
            print('converted')
    else:
        try:
            import converter  # deferred import
            j = converter.convert(os.path.join('grib-data', stamp + '.f000'))
            with open(os.path.join('backend', 'data', 'latest.json'), 'w') as f:
                json.dump(j, f)
            print('converted')
        except ModuleNotFoundError as e:
            print(e)
            print("\n\tpygrib is not supported on Windows, please use '-j' to use grib2json\n")


def roundHour(hour, interval) -> str:
    if interval > 0:
        result = (math.floor(hour / interval) * interval)
        return str(result) if result >= 10 else '0' + str(result)


if __name__ == '__main__':
    main()

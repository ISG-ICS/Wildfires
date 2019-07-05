import requests
from datetime import datetime, timedelta
import math
import os
import subprocess

# baseDir = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_1p00.pl'
baseDir = 'http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl'


def main():
    t = datetime.today()
    runQuery(t - timedelta(hours=0))


def runQuery(t):
    time = t.timetuple()
    date = t.strftime('%Y%m%d')
    hour = roundHour(time.tm_hour, 6)
    stamp = date + hour
    stamp2 = date + '/' + hour

    # qs = {
    #     'file': 'gfs.t' + hour + 'z.pgrb2.1p00.f000',
    #     'lev_10_m_above_ground': 'on',
    #     'lev_surface': 'on',
    #     'var_TMP': 'on',
    #     'var_UGRD': 'on',
    #     'var_VGRD': 'on',
    #     'leftlon': 0,
    #     'rightlon': 360,
    #     'toplat': 90,
    #     'bottomlat': -90,
    #     'dir': '/gfs.' + stamp2
    # }

    qs = {
        'file': 'gfs.t' + hour + 'z.pgrb2.0p25.anl',
        'lev_10_m_above_ground': 'on',
        'lev_surface': 'on',
        'var_TMP': 'on',
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
            print(stamp + ' not found')
            runQuery(t - timedelta(hours=6))
        else:
            if not os.path.isdir('grib-data'):
                os.makedirs('grib-data')
            if not os.path.isdir('json-data'):
                os.makedirs('json-data')
            with open(os.path.join('grib-data', stamp + '.f000'), 'wb') as f:
                f.write(r.content)
            print('saved')

            # convert format
            cmd = [os.path.join('converter', 'bin', 'grib2json'), '--data', '--output', 'json-data/' + stamp + '.json',
                   '--names',
                   '--compact', 'grib-data/' + stamp + '.f000']
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            process.wait()
            if process.returncode == 0:
                print('converted')
    except IOError as e:
        print(e)
        runQuery(t - timedelta(hours=6))


def roundHour(hour, interval) -> str:
    if interval > 0:
        result = (math.floor(hour / interval) * interval)
        return str(result) if result >= 10 else '0' + str(result)


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

import psycopg2
from extract_moisture_data import GRIBExtractor


class moisture_dumper:
    def __init__(self):
        self.conn = psycopg2.connect(dbname="testdb", user="tester", password="testpassword",
                                     host="cloudberry05.ics.uci.edu", port="5432")

    def extract_and_dump(self):
        path = "moisture_data"
        files = os.listdir(path)
        for file in files:
            if not os.path.isdir(file) and 'txt' in file:
                file = path + '/' + file
                grib_extractor = GRIBExtractor(file, 'Liquid volumetric soil moisture (non-frozen)', 0, 10)
                dictionary = grib_extractor.extract('Liquid volumetric soil moisture (non-frozen)', 0, 10)
                time = file[file.find('grib2_') + 6:file.find('.txt')]
                for key, value in dictionary.items():
                    lat = float(key[1:key.find(',')])
                    long = float(key[key.find(',') + 1:key.find(')')])
                    value = float(value)
                    if str(value) != 'nan':
                        self.dump_data(lat, long, value, time)
                        print('dump successfully')

    def dump_data(self, p_lat, p_long, p_value, p_time):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO moisture(lat,long,moisture,datetime) values (%s, %s, %s, %s)",
                    (p_lat, p_long, p_value, p_time))
        self.conn.commit()
        cur.close()


if __name__ == '__main__':
    moisture_dumper().extract_and_dump()
    # conn = psycopg2.connect(dbname="testdb", user="tester", password="testpassword",
    #                         host="cloudberry05.ics.uci.edu", port="5432")
    # cur = conn.cursor()
    # cur.execute("delete from moisture")
    # conn.commit()
    # cur.close()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import datetime
import os
import psycopg2
import rootpath
rootpath.append()
from configurations import REC_TEMP_MOIS_PATH
from extract_mois_temp_data import GRIBExtractor, TIFExtractor
from backend.data_preparation.dumper.dumperbase import DumperBase

class MoistureTemperatureDumper(DumperBase):

    def insert_one(self, conn, p_lat, p_long, p_value, p_time=0, p_start=0, p_end=0, attri_name=''):
        # insert one record into database
        # recording insert count number to self.inserted_count

        if p_lat > 49 or p_lat < 25 or p_long < 230 or p_long > 290:
            return

        cur = conn.cursor()
        if attri_name == 'rec_temp':
            cur.execute(
                "INSERT INTO recent_temperature(lat,long,temperature,starttime,endtime) values (%s, %s, %s, %s, %s)",
                (p_lat, p_long, p_value, p_start, p_end))
        if attri_name == 'rec_mois':
            cur.execute("INSERT INTO recent_moisture(lat,long,moisture,starttime, endtime) values (%s, %s, %s, %s, %s)",
                        (p_lat, p_long, p_value, p_start, p_end))
        if attri_name == 'his_temp':
            cur.execute("INSERT INTO historical_temperature(lat,long,temperature,datetime) values (%s, %s, %s, %s)",
                        (p_lat, p_long, p_value, p_time))
        if attri_name == 'his_mois':
            cur.execute("INSERT INTO historical_moisture(lat,long,moisture,datetime) values (%s, %s, %s, %s)",
                        (p_lat, p_long, p_value, p_time))
        self.conn.commit()
        cur.close()


    def insert_batch(*args, **kwargs):
        # insert a batch of records into database
        # recording insert count number to self.inserted_count
        pass
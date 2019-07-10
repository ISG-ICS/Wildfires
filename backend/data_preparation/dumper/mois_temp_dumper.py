#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import rootpath

rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase


class MoisTempDumper(DumperBase):
    HIS_TEMP_MODE = 0
    HIS_MOIS_MODE = 1
    REC_TEMP_MODE = 2
    REC_MOIS_MODE = 3

    def insert(self, data):
        # insert one record into database
        # recording insert count number to self.inserted_count

        # filter for geolocation in America
        if data["p_lat"] > 49 or data["p_lat"] < 25 or data["p_long"] < 230 or data["p_long"] > 290:
            return

        cur = data["conn"].cursor()
        try:
            if data["data_type"] == MoisTempDumper.REC_TEMP_MODE:
                cur.execute(
                    "INSERT INTO recent_temperature(lat,long,temperature,starttime,endtime) values (%s, %s, %s, %s, %s)",
                    (data["p_lat"], data["p_long"], data["p_value"], data["p_start"], data["p_end"]))
            if data["data_type"] == MoisTempDumper.REC_MOIS_MODE:
                cur.execute(
                    "INSERT INTO recent_moisture(lat,long,moisture,starttime, endtime) values (%s, %s, %s, %s, %s)",
                    (data["p_lat"], data["p_long"], data["p_value"], data["p_start"], data["p_end"]))
            if data["data_type"] == MoisTempDumper.HIS_TEMP_MODE:
                cur.execute("INSERT INTO historical_temperature(lat,long,temperature,datetime) values (%s, %s, %s, %s)",
                            (data["p_lat"], data["p_long"], data["p_value"], data["p_time"]))

            if data["data_type"] == MoisTempDumper.HIS_MOIS_MODE:
                cur.execute("INSERT INTO historical_moisture(lat,long,moisture,datetime) values (%s, %s, %s, %s)",
                            (data["p_lat"], data["p_long"], data["p_value"], data["p_time"]))
        except Exception as err:
            print("error", err)

        data["conn"].commit()
        cur.close()
        self.inserted_count += 1

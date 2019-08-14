import os
import logging
import traceback
import rootpath
import paths
from PIL import Image
import numpy as np

rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')


class SoilMoisDumper(DumperBase):
    INSERT_SOIL_MOISTURE = 'INSERT INTO env_soil_moisture (gid, datetime, soil_moisture) ' \
                           'VALUES (%s, %s, %s)'

    def insert(self, datetime: str, weekly_soil_mois: list):
        gid = 0

        with Connection() as conn:
            cur = conn.cursor()

            for i in range(len(weekly_soil_mois)):
                for j in range(len(weekly_soil_mois[i])):

                    weekly_soil_mois_value = weekly_soil_mois[i][j]

                    try:
                        cur.execute(SoilMoisDumper.INSERT_SOIL_MOISTURE,
                                    (gid, datetime, weekly_soil_mois_value))
                    except Exception:
                        logger.error("error: " + traceback.format_exc())

                    gid += 1

            conn.commit()
            cur.close()

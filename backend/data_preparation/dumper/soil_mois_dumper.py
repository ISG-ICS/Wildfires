import logging
import traceback
from typing import List

import rootpath

rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')


class SoilMoisDumper(DumperBase):
    INSERT_SOIL_MOISTURE = "INSERT INTO env_soil_moisture (gid, datetime, soil_moisture) " \
                           "VALUES (%s, %s, %s) ON CONFLICT (gid, datetime) DO UPDATE SET soil_moisture=float 'NaN'"

    def insert(self, datetime: str, weekly_soil_mois: List[List[float]]):
        gid = 0

        with Connection() as conn:
            cur = conn.cursor()

            for row in weekly_soil_mois:
                for weekly_soil_mois_value in row:
                    if weekly_soil_mois_value in [-999, -9999]:
                        weekly_soil_mois_value = float('NaN')
                    try:
                        cur.execute(self.INSERT_SOIL_MOISTURE,
                                    (gid, datetime, weekly_soil_mois_value))
                        self.inserted_count += cur.rowcount
                        conn.commit()
                    except Exception:
                        logger.error("error: " + traceback.format_exc())
                    gid += 1
            logger.info(f'{datetime} finished, total inserted {self.inserted_count}')
            cur.close()

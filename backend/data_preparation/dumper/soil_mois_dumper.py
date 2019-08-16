import datetime
import logging
import traceback

import numpy as np
import rootpath

from backend.data_preparation.crawler.soil_mois_crawler import SoilMoisCrawler
from backend.data_preparation.extractor.soil_mois_extractor import SoilMoisExtractor

rootpath.append()

from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')


class SoilMoisDumper(DumperBase):
    INSERT_SOIL_MOISTURE = "INSERT INTO env_soil_moisture (gid, datetime, soil_moisture) " \
                           "VALUES (%s, %s, %s) ON CONFLICT (gid, datetime) DO NOTHING"

    def insert(self, date_str: str, weekly_soil_mois: np.array):

        flattened_data = weekly_soil_mois.flatten()

        print(flattened_data)
        with Connection() as conn:
            cur = conn.cursor()
            for gid, val in enumerate(flattened_data.tolist()):
                val = float('NaN') if val in [-999, -9999] else val
                try:
                    cur.execute(self.INSERT_SOIL_MOISTURE, (gid, datetime.datetime.strptime(date_str, "%Y%m%d"), val))
                    self.inserted_count += cur.rowcount
                    conn.commit()
                except Exception:
                    logger.error("error: " + traceback.format_exc())

            logger.info(f'{datetime} finished, total inserted {self.inserted_count}')
            cur.close()


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    crawler = SoilMoisCrawler()
    stamp = crawler.crawl(datetime.datetime.strptime("20131230", "%Y%m%d"))
    extractor = SoilMoisExtractor()
    data = extractor.extract(stamp)
    dumper = SoilMoisDumper()
    dumper.insert("20131230", data)

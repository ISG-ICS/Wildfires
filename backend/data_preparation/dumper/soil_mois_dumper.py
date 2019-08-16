import datetime
import logging
import traceback

import numpy as np
import rootpath

rootpath.append()
from backend.data_preparation.crawler.soil_mois_crawler import SoilMoisCrawler
from backend.data_preparation.extractor.soil_mois_extractor import SoilMoisExtractor
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')


class SoilMoisDumper(DumperBase):
    INSERT_SOIL_MOISTURE = "INSERT INTO env_soil_moisture (gid, datetime, soil_moisture) " \
                           "VALUES (%s, %s, %s) ON CONFLICT (gid, datetime) DO NOTHING"

    def insert(self, date_str: str, weekly_soil_mois: np.array):
        flattened_data = weekly_soil_mois.flatten()
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

            logger.info(f'{date_str} finished, total inserted {self.inserted_count}')
            cur.close()


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    crawler = SoilMoisCrawler()
    file_path = crawler.crawl(datetime.datetime.strptime("20131230", "%Y%m%d"))
    extractor = SoilMoisExtractor()
    data = extractor.extract(file_path)
    dumper = SoilMoisDumper()
    date_str = file_path.split('_')[-1].split('.')[0].split('/')[-1]
    dumper.insert(date_str, data)

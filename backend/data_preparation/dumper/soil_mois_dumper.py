"""
@author: Tingxuan Gu
"""
import datetime
import logging
import traceback

import numpy as np

from utilities.connection import Connection
from .dumperbase import DumperBase

logger = logging.getLogger('TaskManager')


class SoilMoisDumper(DumperBase):
    """
    This class is responsible for dumping extracted NASAGrace data into database
    """
    TIME_FORMAT = "%Y%m%d"
    INSERT_SOIL_MOISTURE = "INSERT INTO env_soil_moisture (gid, datetime, soil_moisture) " \
                           "VALUES (%s, %s, %s) ON CONFLICT (gid, datetime) DO UPDATE " \
                           "SET soil_moisture = excluded.soil_moisture"

    def insert(self, date_str: str, weekly_soil_mois: np.array) -> None:
        """
        :param date_str: current data's datetime
        :param weekly_soil_mois: data
        :return: None
        """
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
    from data_preparation.crawler.soil_mois_crawler import SoilMoisCrawler
    from data_preparation.extractor.soil_mois_extractor import TiffExtractor

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    crawler = SoilMoisCrawler()
    extractor = TiffExtractor()
    dumper = SoilMoisDumper()
    target_time = "20131230"

    crawled_file_path = crawler.crawl(datetime.datetime.strptime(target_time, SoilMoisDumper.TIME_FORMAT))
    if crawled_file_path is not None:
        data = extractor.extract(crawled_file_path)
        dumper.insert(target_time, data)

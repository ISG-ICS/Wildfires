import datetime
import logging
import os
import zipfile

import numpy as np
import psycopg2.errors
import psycopg2.extras

from data_preparation.dumper.dumperbase import DumperBase
from utilities.connection import Connection

logger = logging.getLogger('TaskManager')


class PRISMDumper(DumperBase):
    INSERT_SQLS = {
        'ppt': '''
                insert into prism (date, gid, ppt) values %s
                ON CONFLICT (date, gid) DO UPDATE SET
                ppt=EXCLUDED.ppt
            ''',
        'tmax': '''
                insert into prism (date, gid, tmax) values %s
                ON CONFLICT (date, gid) DO UPDATE SET
                tmax=EXCLUDED.tmax
            ''',
        'vpdmax': '''
                insert into prism (date, gid, vpdmax) values %s
                ON CONFLICT (date, gid) DO UPDATE SET
                vpdmax=EXCLUDED.vpdmax
            ''',
        'usgs': '''
                insert into usgs (date, gid, usgs) values %s
                ON CONFLICT (date, gid) DO UPDATE SET
                usgs=EXCLUDED.usgs
            '''
    }
    INSERT_INFOS = {
        'ppt': 'insert into prism_info (date, ppt) values (%s, %s) '
               'on conflict(date) do update set ppt=EXCLUDED.ppt',
        'tmax': 'insert into prism_info (date, tmax) values (%s, %s) '
                'on conflict(date) do update set tmax=EXCLUDED.tmax',
        'vpdmax': 'insert into prism_info (date, vpdmax) values (%s, %s) '
                  'on conflict(date) do update set vpdmax=EXCLUDED.vpdmax',
        'usgs': 'insert into usgs_info (date) values (%s)'
                'on conflict(date) do nothing'
    }

    def insert(self, date: datetime.date, unflattened_data: np.ndarray, var_type: str):
        """

        :param date: datetime.date
        :param unflattened_data: numpy.ndarray
        :param var_type: string
        :return: None
        """
        flattened = unflattened_data.flatten()
        with Connection() as conn:
            cur = conn.cursor()
            psycopg2.extras.execute_values(cur, PRISMDumper.INSERT_SQLS[var_type],
                                           PRISMDumper.record_generator(date, flattened),
                                           template=None, page_size=10000)
            if var_type == 'usgs':
                cur.execute(PRISMDumper.INSERT_INFOS[var_type], (date,))
            else:
                cur.execute(PRISMDumper.INSERT_INFOS[var_type], (date, 1))
            conn.commit()
            cur.close()

    @staticmethod
    def record_generator(date: datetime.date, _data):
        for gid, val in enumerate(_data.tolist()):
            yield (date, gid, val)


if __name__ == '__main__':
    from data_preparation.crawler.usgs_crawler import USGSCrawler

    from data_preparation.extractor.soil_mois_extractor import TiffExtractor

    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())

    crawler = USGSCrawler()
    extractor = TiffExtractor()
    dumper = PRISMDumper()
    target_time = "20190806"

    zip_file_path = crawler.crawl(datetime.datetime.strptime(target_time, '%Y%m%d'))
    zf = zipfile.ZipFile(zip_file_path)
    for file in zf.namelist():
        if file.split('.')[-4] == 'VI_NDVI' and file.split('.')[-1] == 'tif':
            zf.extract(file, os.path.split(zip_file_path)[0])
            tif_file_name = file
    zf.close()
    tif_path = os.path.join(os.path.split(zip_file_path)[0], tif_file_name)

    if tif_path is not None:
        data = extractor.extract(tif_path)
        dumper.insert(datetime.datetime.strptime(target_time, '%Y%m%d'), data, var_type='usgs')

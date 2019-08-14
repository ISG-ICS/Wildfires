import datetime
import logging

import numpy as np
import psycopg2.errors
import psycopg2.extras
import rootpath

rootpath.append()
from backend.data_preparation.connection import Connection
from backend.data_preparation.dumper.dumperbase import DumperBase

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
            '''
    }
    INSERT_INFOS = {
        'ppt': 'insert into prism_info (date, ppt) values (%s, %s) '
               'on conflict(date) do update set ppt=EXCLUDED.ppt',
        'tmax': 'insert into prism_info (date, tmax) values (%s, %s) '
                'on conflict(date) do update set tmax=EXCLUDED.tmax',
        'vpdmax': 'insert into prism_info (date, vpdmax) values (%s, %s) '
                  'on conflict(date) do update set vpdmax=EXCLUDED.vpdmax'
    }

    def insert(self, date: datetime.date, _data: np.ndarray, var_type: str):
        with Connection() as conn:
            cur = conn.cursor()
            psycopg2.extras.execute_values(cur, PRISMDumper.INSERT_SQLS[var_type],
                                           PRISMDumper.record_generator(date, _data),
                                           template=None, page_size=10000)
            cur.execute(PRISMDumper.INSERT_INFOS[var_type], (date, 1))
            conn.commit()
            cur.close()

    @staticmethod
    def record_generator(date: datetime.date, _data):
        for gid, val in enumerate(_data.tolist()):
            yield (date, gid, val)

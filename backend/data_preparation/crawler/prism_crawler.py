import logging
import os
from datetime import datetime, timedelta, timezone
from ftplib import FTP, error_perm
from typing import List, Union

import rootpath

rootpath.append()

from paths import PRISM_DATA_PATH
from backend.data_preparation.connection import Connection
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.extractor.bil_extractor import BILExtractor, BILFormat
from backend.data_preparation.dumper.prism_dumper import PRISMDumper

logging.getLogger('TaskManager')


class PRISMCrawler(CrawlerBase):
    ftp_server = 'prism.nacse.org'
    variables = ['ppt', 'tmax', 'vpdmax']
    stages = ['stable', 'provisional', 'early']
    addition_codes = {
        'ppt': '4kmD2',
        'tmax': '4kmD1',
        'vpdmax': '4kmD1'
    }

    def __init__(self):
        super().__init__()
        self.current_date = datetime.now(timezone.utc).date()

        self.ftp = FTP(PRISMCrawler.ftp_server)
        self.ftp.login('anonymous')
        self.buffer: List[bytes] = list()

    def crawl(self, date: datetime.date, variable) -> Union[str, None]:
        """this func will download a single file"""
        if not os.path.exists(PRISM_DATA_PATH):
            os.makedirs(PRISM_DATA_PATH)

        self.ftp.cwd(f'/daily/{variable}/{date.strftime("%Y")}')
        for stage in PRISMCrawler.stages:
            filename = f'PRISM_{variable}_{stage}_{PRISMCrawler.addition_codes[variable]}' \
                f'_{date.strftime("%Y%m%d")}_bil.zip'
            try:
                self.ftp.retrbinary(f"RETR {filename}", self.assign_buffer)
            except error_perm as e:
                print(e)
                continue
            else:
                self.buffer = b''.join(self.buffer)
                with open(os.path.join(PRISM_DATA_PATH, filename), 'wb') as f:
                    f.write(self.buffer)
                self.buffer = list()
                print('write')
                return os.path.join(PRISM_DATA_PATH, filename)

        # return None if not crawled
        return None

    def start(self, end_clause: datetime.date = None, *args, **kwargs) -> None:
        """this func will start a round of crawling.
            based on RECENT or HISTORICAL
        """

        with Connection() as conn:
            cur = conn.cursor()
            cur.execute('select date, ppt, tmax, vpdmax from prism_info')
            exist_list = cur.fetchall()

            exist_dict = dict()
            for date, ppt, tmax, vpdmax in exist_list:
                exist_dict[date] = (ppt, tmax, vpdmax)

        date = self.current_date - timedelta(days=1)
        while date >= end_clause:

            print(f'fetch: {date}')
            # var_dict = dict()
            for var_idx, var in enumerate(PRISMCrawler.variables):
                # skip if exist
                if date in exist_dict and exist_dict[date][var_idx]:
                    print(f'skip: {date}-{var}')
                    continue

                saved_filepath = self.crawl(date, var)
                if saved_filepath:
                    # noinspection PyTypeChecker
                    bil = self.extractor.extract(saved_filepath)  # type: BILFormat
                    self.dumper.insert(date, bil.flattened, var)
                    # var_dict[var] = bil.flattened

                    # clean up
                    os.remove(saved_filepath)

            # table = PRISMCrawler.merge_table(date, var_dict)
            # finish crawling a day
            date = date - timedelta(days=1)

    def assign_buffer(self, content) -> None:
        self.buffer.append(content)

    @staticmethod
    def merge_table(date: datetime.date, var_dict: dict):
        return [(date, gid, var_dict['ppt'][gid], var_dict['tmax'][gid], var_dict['vpdmax'][gid]) for gid in
                range(len(var_dict['ppt']))]


if __name__ == '__main__':
    crawler = PRISMCrawler()
    crawler.set_extractor(BILExtractor())
    crawler.set_dumper(PRISMDumper())
    crawler.start(datetime.now().date() - timedelta(days=7))

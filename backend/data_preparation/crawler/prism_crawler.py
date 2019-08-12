import logging
import os
from datetime import datetime, timedelta, timezone
from ftplib import FTP, error_perm
from typing import List, Union

import numpy as np
import rootpath

rootpath.append()

from paths import PRISM_DATA_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.extractor.bil_extractor import BILExtractor, BILFormat

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

        date = self.current_date - timedelta(days=1)
        while date >= end_clause:
            for var in PRISMCrawler.variables:
                saved_filepath = self.crawl(date, var)
                if saved_filepath:
                    # noinspection PyTypeChecker
                    bil = self.extractor.extract(saved_filepath)  # type: BILFormat
                    np.save(os.path.splitext(saved_filepath)[0], bil.ndarray)
                    # clean up
                    os.remove(saved_filepath)

            # finish crawling a day
            date = date - timedelta(days=1)

    def assign_buffer(self, content) -> None:
        self.buffer.append(content)


if __name__ == '__main__':
    crawler = PRISMCrawler()
    crawler.set_extractor(BILExtractor())
    crawler.start(datetime.now().date() - timedelta(days=7))

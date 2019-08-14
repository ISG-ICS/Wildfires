import logging
import os
from datetime import timedelta, date
from ftplib import FTP, error_perm
from typing import List, Optional

import rootpath

rootpath.append()

from paths import PRISM_DATA_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase

logger = logging.getLogger('TaskManager')


class PRISMCrawler(CrawlerBase):
    FTP_SERVER = 'prism.nacse.org'
    VARIABLES = ['ppt', 'tmax', 'vpdmax']
    STAGES = ['stable', 'provisional', 'early']
    ADDITIONAL_CODES = {
        'ppt': '4kmD2',
        'tmax': '4kmD1',
        'vpdmax': '4kmD1'
    }

    def __init__(self):
        super().__init__()

        self.ftp = FTP(PRISMCrawler.FTP_SERVER)
        self.ftp.login('anonymous')
        self.buffer: List[bytes] = list()

    def crawl(self, target_date: date, variable: str) -> Optional[str]:
        """this func will download a single file"""
        if not os.path.exists(PRISM_DATA_PATH):
            os.makedirs(PRISM_DATA_PATH)

        self.ftp.cwd(f'/daily/{variable}/{target_date.strftime("%Y")}')
        for stage in PRISMCrawler.STAGES:
            filename = f'PRISM_{variable}_{stage}_{PRISMCrawler.ADDITIONAL_CODES[variable]}' \
                       f'_{target_date.strftime("%Y%m%d")}_bil.zip'
            try:
                self.ftp.retrbinary(f"RETR {filename}", lambda content: self.buffer.append(content))
            except error_perm as e:
                logger.info(e)
                continue
            else:
                zip_content = b''.join(self.buffer)
                with open(os.path.join(PRISM_DATA_PATH, filename), 'wb') as f:
                    f.write(zip_content)
                self.buffer.clear()
                logger.info(f'file-written: {filename}')
                return os.path.join(PRISM_DATA_PATH, filename)

        # return None if not crawled
        return None


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    crawler = PRISMCrawler()
    crawler.crawl(date.today() - timedelta(days=1), 'ppt')

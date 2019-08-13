import logging
import os
from datetime import datetime, timedelta
from ftplib import FTP, error_perm
from typing import List, Optional

import rootpath

rootpath.append()

from paths import PRISM_DATA_PATH
from backend.data_preparation.crawler.crawlerbase import CrawlerBase
from backend.data_preparation.extractor.bil_extractor import BILExtractor
from backend.data_preparation.dumper.prism_dumper import PRISMDumper

logger = logging.getLogger('TaskManager')


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

        self.ftp = FTP(PRISMCrawler.ftp_server)
        self.ftp.login('anonymous')
        self.buffer: List[bytes] = list()

    def crawl(self, date: datetime.date, variable) -> Optional[str]:
        """this func will download a single file"""
        if not os.path.exists(PRISM_DATA_PATH):
            os.makedirs(PRISM_DATA_PATH)

        self.ftp.cwd(f'/daily/{variable}/{date.strftime("%Y")}')
        for stage in PRISMCrawler.stages:
            filename = f'PRISM_{variable}_{stage}_{PRISMCrawler.addition_codes[variable]}' \
                f'_{date.strftime("%Y%m%d")}_bil.zip'
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

    def start(self, end_clause: datetime.date = None, *args, **kwargs) -> None:
        pass


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    crawler = PRISMCrawler()
    crawler.set_extractor(BILExtractor())
    crawler.set_dumper(PRISMDumper())
    crawler.start(datetime.now().date() - timedelta(days=7))

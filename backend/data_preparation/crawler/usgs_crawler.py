import logging
import os
from datetime import timedelta, date
from typing import Optional

import requests
import requests.cookies
from dateutil import parser as date_parser
from lxml import html

from data_preparation.crawler.crawlerbase import CrawlerBase
from utilities.paths import USGS_DATA_DIR

logger = logging.getLogger('TaskManager')


class USGSCrawler(CrawlerBase):
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

        # cookie may expire in 7days or 2hrs. not sure
        self.session = requests.Session()

        # 1. fetch login page, get _csrf_token
        login_page = self.session.get('https://ers.cr.usgs.gov/login/')
        html_root = html.fromstring(login_page.content)  # type: html.HtmlElement
        csrf, = html_root.xpath('//*[@id="csrf_token"]')  # type: html.HtmlElement
        ncforminfo, = html_root.xpath('//*[@id="loginForm"]/input[2]')  # type: html.HtmlElement
        csrf_token = csrf.get('value')
        __ncforminfo = ncforminfo.get('value')

        p = self.session.post('https://ers.cr.usgs.gov/login/',
                              headers={"Content-type": "application/x-www-form-urlencoded",
                                       'Referer': 'https://ers.cr.usgs.gov/login/',
                                       'Origin': 'https://ers.cr.usgs.gov'
                                       },
                              data={
                                  "username": "ardentlyhickstead",
                                  "password": "testpassword2",
                                  "csrf_token": csrf_token,
                                  '__ncforminfo': __ncforminfo
                              }, allow_redirects=False)

        # print the html returned or something more intelligent to see if it's a successful login page.
        logger.info(f'[login]{p}')

    def crawl(self, target_date: date) -> Optional[str]:
        """
            this func will download a single file
            target_date should be 7-day interval with 2019-07-30
        """

        if not os.path.exists(USGS_DATA_DIR):
            os.makedirs(USGS_DATA_DIR)

        stamp = target_date.strftime('%Y%m%d') + (target_date + timedelta(days=6)).strftime('%Y%m%d')
        filename = f'EMUSA{stamp}6.zip'

        try:
            logger.info(f'[downloading]{filename}')
            # An authorised request.
            response = self.session.get(f'https://earthexplorer.usgs.gov/download/13121/EMUSA{stamp}6/NDVI1KM/EE',
                                        allow_redirects=False)
            response = self.session.send(response.next)
        except Exception as e:
            logger.error(e)
            # return None if not crawled
            return None
        else:
            # report error if not 200
            if response.status_code != 200:
                logger.error(f'[failed]{filename} http-code={response.status_code}')
                logger.warning(f'[failed]{filename} http-code={response.status_code}')
                return None

            # write and return full path of zip-file
            with open(os.path.join(USGS_DATA_DIR, filename), 'wb') as f:
                f.write(response.content)
            logger.info(f'[file-written]{filename}')
            return os.path.join(USGS_DATA_DIR, filename)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    crawler = USGSCrawler()
    crawler.crawl(date_parser.parse('20190730').date())

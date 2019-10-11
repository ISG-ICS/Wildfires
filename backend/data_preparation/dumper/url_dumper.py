import logging
from typing import Union, List, Dict, Generator, Tuple

import rootpath

rootpath.append()
from backend.connection import Connection
from backend.data_preparation.dumper.dumperbase import DumperBase

logger = logging.getLogger('TaskManager')


class URLDumper(DumperBase):
    def insert(self, data: Union[List, Dict]):
        if isinstance(data, dict):
            Connection().sql_execute_values("insert into images(id,image_url) values ", self._gen_id_url_pair(data))

    @staticmethod
    def _gen_id_url_pair(data) -> Generator[Tuple[int, str], None, None]:
        for tid, urls in data.items():
            for url in urls:
                yield tid, url

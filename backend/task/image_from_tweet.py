import logging
import traceback

from data_preparation.dumper.url_dumper import URLDumper
from data_preparation.extractor.tweet_media_extractor import TweetMediaExtractor
from task.runnable import Runnable
from utilities.connection import Connection

logger = logging.getLogger('TaskManager')


class ImageFromTweet(Runnable):

    def __init__(self):
        self.extractor = TweetMediaExtractor()
        self.dumper = URLDumper()

    def run(self, batch_num: int = 100):
        try:
            self.dumper.insert({id: self.extractor.extract(text) for id, text in
                                Connection().sql_execute(
                                    f"select id, text from records r WHERE NOT EXISTS (select distinct id from images i where i.id = r.id) limit {batch_num}")})
        except Exception:
            logger.error('error: ' + traceback.format_exc())


if __name__ == '__main__':
    while True:
        ImageFromTweet().run()

import logging
import traceback

import rootpath

rootpath.append()
from backend.task.runnable import Runnable
from backend.connection import Connection
from backend.classifiers.text_classifier import TextClassifier
from backend.data_preparation.dumper.text_classification_dumper import TextClassificationDumper
from paths import TEXT_CNN_MODEL_PATH

logger = logging.getLogger('TaskManager')


class TextClassification(Runnable):

    def run(self):
        try:
            """get tweets from database and dump prediction results into database"""
            # set up text classifier
            text_classifier = TextClassifier()

            # use the pre-trained model
            text_classifier.set_model(TEXT_CNN_MODEL_PATH)

            # set up text dumper
            text_dumper = TextClassificationDumper()

            # loop required text in database
            for tweet_id, text in Connection().sql_execute(
                    "select id, text from records where text_cnn_wildfire_prob is null"):
                # preprocess the text
                processed_text = text_classifier.preprocess(text)
                # get prediction result of text, tuple example: tensor([[0.8321, 0.1679]])
                prediction_tuple = text_classifier.predict(processed_text)
                # dump prediction result into database
                text_dumper.insert(tweet_id, prediction_tuple[0][0].item(), prediction_tuple[0][1].item())
                logger.info("id " + str(tweet_id) + " is done!")
                logger.info("Total affected records: " + str(text_dumper.inserted_count))
        except Exception:
            logger.error('error: ' + traceback.format_exc())


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    logger.addHandler(logging.StreamHandler())
    text_classification = TextClassification()
    text_classification.run()

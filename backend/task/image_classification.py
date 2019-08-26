import logging
import traceback

import rootpath

rootpath.append()
from backend.task.runnable import Runnable
from backend.data_preparation.connection import Connection
from backend.classifiers.image_classifier import ImageClassifier
from backend.data_preparation.dumper.img_classification_dumper import ImgClassificationDumper

logger = logging.getLogger('TaskManager')


class ImageClassification(Runnable):
    """
    Runnable class for tweet images classification. Uses either VGG model or Resnet model to classify each image.
    And dumps classification result into database.
    """

    def run(self, model_type: str = ImageClassifier.RESNET_MODEL):
        """
        Gets image_id and image_url from database and dump prediction results into database.
        :param model_type: different model will be used according to model type.
        :return: none
        """
        # set up image classifier
        image_classifier = ImageClassifier(model_type)

        image_classifier.set_model()

        # set up event2mindDumper
        img_classification_dumper = ImgClassificationDumper()

        # loop every image in database
        try:
            for id, image_url in Connection().sql_execute("select id, image_url from images"):
                # get prediction result of image
                prediction_tuple = image_classifier.predict(image_url)
                # dump prediction result into database
                img_classification_dumper.insert(model_type, image_url, prediction_tuple)
                logger.info("id " + str(id) + " is done!")
        except:
            logger.error('error: ' + traceback.format_exc())


if __name__ == '__main__':
    image_classification = ImageClassification()
    # model type can be specified to VGG or ResNet, choose one to run
    image_classification.run(model_type=ImageClassifier.VGG_MODEL)
    image_classification.run(model_type=ImageClassifier.RESNET_MODEL)

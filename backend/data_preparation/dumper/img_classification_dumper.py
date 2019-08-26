import logging
import traceback
from typing import Tuple

import rootpath

rootpath.append()
from backend.data_preparation.dumper.dumperbase import DumperBase
from backend.classifiers.image_classifier import ImageClassifier
from backend.data_preparation.connection import Connection

logger = logging.getLogger('TaskManager')


class ImgClassificationDumper(DumperBase):

    def insert(self, model_type: str, image_url: str, data: Tuple[float, float]) -> None:
        """
        Inserts image prediction result into images table.
        :param model_type: vgg or resnet for image classification model.
        :param image_url: image's url that identify each distinct image.
        :param data: image prediction result -- probability of being wildfire and not wildfire.
        """
        # extract data to be dumped
        prob_not_wildfire, prob_wildfire = data

        # for vgg model
        if model_type == ImageClassifier.VGG_MODEL:
            try:
                Connection().sql_execute_commit(
                    f"UPDATE images SET not_wildfire_prob = {prob_not_wildfire}, wildfire_prob = {prob_wildfire} "
                    f"WHERE image_url = {repr(image_url)}")

            except Exception:
                logger.error("error: " + traceback.format_exc())

        # for resnet model
        elif model_type == ImageClassifier.RESNET_MODEL:
            try:
                Connection().sql_execute_commit(
                    f"UPDATE images SET resnet_not_wildfire = {prob_not_wildfire}, resnet_wildfire = {prob_wildfire} "
                    f"WHERE image_url = {repr(image_url)}")

            except Exception:
                logger.error("error: " + traceback.format_exc())
        else:
            logger.error("Insertion fail. Please specify the model type to be vgg or resnet.")


if __name__ == '__main__':
    # test case
    ImgClassificationDumper().insert(model_type=ImageClassifier.VGG_MODEL,
                                     image_url='https://pbs.twimg.com/media/Dd2c4mlUwAAolWC.jpg', data=[0.0, 1.0])